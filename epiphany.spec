%define dirver 2.30
%define webkit 1.1.17

Summary: GNOME web browser based on the webkit rendering engine
Name: epiphany
Version: 2.29.3
Release: %mkrel 1
License: GPLv2+ and GFDL
Group: Networking/WWW
URL: http://www.gnome.org/projects/epiphany/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
#gw fix crash in password migration from old xulrunner backend
#https://bugzilla.gnome.org/show_bug.cgi?id=594717
Patch: epiphany-fix-password-migration.patch
# (fc) 0.9.2-2mdk fix defaults settings
Patch1:	epiphany-2.24.2.1-defaults.patch
# (fc) 1.4.6-2mdk default bookmarks
Patch6: epiphany-defaultbookmarks.patch
# (fc) 1.8.5-4mdk set urpmi and bundles mimetypes as safe (Mdk bug #21892)
Patch9: epiphany-1.8.5-urpmi.patch
Patch10: epiphany-2.27.0-fix-str-fmt.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: webkitgtk-devel >= %webkit
BuildRequires: libsoup-devel >= 2.27.91
BuildRequires: gtk2-devel >= 2.15.1
BuildRequires: gnome-desktop-devel >= 2.10.0
BuildRequires: iso-codes
BuildRequires: libxslt-devel
BuildRequires: dbus-devel >= 0.35
BuildRequires: avahi-gobject-devel
BuildRequires: libnotify-devel
BuildRequires: nss-devel
BuildRequires: scrollkeeper
BuildRequires: gtk-doc
BuildRequires: intltool
BuildRequires: gnome-common
BuildRequires: gnome-doc-utils >= 0.3.2
BuildRequires: librsvg
BuildRequires: imagemagick
BuildRequires: desktop-file-utils
BuildRequires: autoconf2.5
BuildRequires: automake

Requires(post): scrollkeeper
Requires(postun): scrollkeeper
Provides:       webclient
#gw for the index themes
Requires: gnome-themes
Requires: gnome-doc-utils >= 0.3.2
Requires: indexhtml
Requires: iso-codes
Requires: dbus-x11
Requires: enchant
Requires: libwebkitgtk >= %webkit

%description
Epiphany is a GNOME web browser based on the webkit
rendering engine.
The name meaning:
"An intuitive grasp of reality through
something (as an event) usually simple and striking"

%package devel
Group: Development/C
Summary: Header files for developing with Epiphany
Requires: libxml2-devel
Requires: libgnomeui2-devel
Requires: libglade2.0-devel
Requires: dbus-devel


%description devel
This contains the C headers required for developing with Epiphany.

%prep
%setup -q
%patch -p1
%patch1 -p1 -b .defaults
%patch6 -p1 -b .defaultbookmarks
%patch9 -p1 -b .urpmi
%patch10 -p1 -b .str

%build

aclocal -Im4
automake
autoconf
%configure2_5x --with-distributor-name=Mandriva \
--disable-scrollkeeper

#remove generated files which shouldn't have been put in the tarball
make clean

%make

%install
rm -rf $RPM_BUILD_ROOT %{name}-2.0.lang

%makeinstall_std

# don't display bookmark editor in menu
echo 'NoDisplay=true' >>$RPM_BUILD_ROOT%{_datadir}/applications/bme.desktop
# don't register bookmark editor in bugzilla, main .desktop is enough
sed -i -e '/^X-GNOME-Bugzilla/d' $RPM_BUILD_ROOT%{_datadir}/applications/bme.desktop

%find_lang %{name}-2.0 --with-gnome --all-name
for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do
echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name-2.0.lang
done

mkdir -p %buildroot{%_liconsdir,%_iconsdir,%_miconsdir}
install -m 644 data/art/epiphany-bookmarks.png %buildroot%_liconsdir/epiphany-bookmarks.png
convert -resize 32x32 data/art/epiphany-bookmarks.png %buildroot%_iconsdir/epiphany-bookmarks.png
convert -resize 16x16 data/art/epiphany-bookmarks.png %buildroot%_miconsdir/epiphany-bookmarks.png

mkdir -p %buildroot%{_datadir}/pixmaps
cp /usr/share/icons/gnome/24x24/apps/web-browser.png %buildroot%{_datadir}/pixmaps/epiphany.png

mkdir -p  %buildroot%{_libdir}/epiphany/%dirver/extensions

#gw these are useless
rm -f %buildroot%{_datadir}/icons/LowContrastLargePrint/*/apps/*

%clean
rm -rf $RPM_BUILD_ROOT

%define schemas epiphany epiphany-lockdown

%post
%if %mdkversion < 200900
%{update_scrollkeeper}
%post_install_gconf_schemas %{schemas}
%endif
if [ "$1" = "2" ]; then
update-alternatives --remove webclient-gnome %{_bindir}/epiphany
update-alternatives --remove webclient-kde %{_bindir}/epiphany
fi
%update_icon_cache hicolor
%update_icon_cache HighContrastLargePrint
%update_icon_cache HighContrastLargePrintInverse

%if %mdkversion < 200900
%{update_menus}
%endif

%preun
%preun_uninstall_gconf_schemas %{schemas}

%postun
%{clean_scrollkeeper}
%{clean_menus}
%clean_icon_cache hicolor
%clean_icon_cache HighContrastLargePrint
%clean_icon_cache HighContrastLargePrintInverse

%files -f %{name}-2.0.lang
%defattr(-,root,root,-)
%doc COPYING.README COPYING README TODO NEWS
%{_sysconfdir}/gconf/schemas/epiphany.schemas
%{_sysconfdir}/gconf/schemas/epiphany-lockdown.schemas
%{_bindir}/*
%{_mandir}/man1/%name.1*
%{_datadir}/applications/*
%{_datadir}/epiphany
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/HighContrastLargePrint/*/apps/*
%{_datadir}/icons/HighContrastLargePrintInverse/*/apps/*
%dir %{_datadir}/omf/epiphany
%{_datadir}/omf/epiphany/epiphany-C.omf
%{_datadir}/dbus-1/services/org.gnome.Epiphany.service
%_liconsdir/*.png
%_iconsdir/*.png
%_miconsdir/*.png
%_datadir/pixmaps/*.png
%dir %_libdir/epiphany
%dir %_libdir/epiphany/%dirver/
%dir %_libdir/epiphany/%dirver/extensions

%files devel
%defattr(-,root,root,-)
%_includedir/*
%_libdir/pkgconfig/*
%_datadir/gtk-doc/html/epiphany
%_datadir/aclocal/*.m4
