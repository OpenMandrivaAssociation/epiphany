%define _requires_exceptions libnspr4\\|libplc4\\|libplds4\\|libnss\\|libsmime3\\|libsoftokn\\|libssl3\\|libgtkembedmoz\\|libxpcom

%define build_with_xulrunner 1
%define build_with_firefox 0
%define build_with_webkit 0

%define with_python 1
%{?_with_python: %global with_python 1}
%{?_without_python: %global with_python 0}

# Build with mozilla instead of firefox
%{?_with_mozilla: %global build_with_firefox 0}
%{?_without_mozilla: %global build_with_firefox 1}


%{?_with_webkit: %global build_with_webkit 1}
%{?_without_webkit: %global build_with_webkit 0}

%define xulrunner 1.9

%define dirver 2.23

Summary: GNOME web browser based on the mozilla rendering engine
Name: epiphany
Version: 2.23.5
Release: %mkrel 3
License: GPLv2+ and GFDL
Group: Networking/WWW
URL: http://www.gnome.org/projects/epiphany/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
# (fc) 0.9.2-2mdk fix defaults settings
Patch1:	epiphany-1.6.4-defaults.patch
# (fc) 1.4.6-2mdk default bookmarks
Patch6: epiphany-defaultbookmarks.patch
# (fc) 1.8.5-4mdk set urpmi and bundles mimetypes as safe (Mdk bug #21892)
Patch9: epiphany-1.8.5-urpmi.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%if %{build_with_webkit}
BuildRequires: webkitgtk-devel
BuildRequires: icu-devel
BuildRequires: sqlite3-devel
%else
%if %build_with_xulrunner
BuildRequires: xulrunner-devel-unstable >= %xulrunner
%else
%if %{build_with_firefox}
BuildRequires: mozilla-firefox-devel
%else
BuildRequires: mozilla-devel
%endif
%endif
%endif
%if %{with_python}
BuildRequires: pygtk2.0-devel >= 2.7.1
BuildRequires: gnome-python-devel
%endif
BuildRequires: gtk2-devel >= 2.9.0
BuildRequires: gnome-desktop-devel >= 2.10.0
BuildRequires: libglade2.0-devel >= 2.3.1
BuildRequires: iso-codes
BuildRequires: libxslt-devel
BuildRequires: dbus-devel >= 0.35
BuildRequires: avahi-gobject-devel
BuildRequires: libnotify-devel
BuildRequires: scrollkeeper
BuildRequires: gtk-doc
BuildRequires: intltool
BuildRequires: gnome-common
BuildRequires: gnome-doc-utils >= 0.3.2
BuildRequires: librsvg
BuildRequires: ImageMagick
BuildRequires: desktop-file-utils
BuildRequires: enchant-devel
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
%if %build_with_xulrunner
Requires: %mklibname xulrunner %xulrunner
%endif
%if %{build_with_firefox}
%define firefox_version %(rpm -q mozilla-firefox --queryformat %{VERSION})
Requires: %mklibname mozilla-firefox %{firefox_version}
%else
%if ! %{build_with_webkit} && ! %build_with_xulrunner
Requires: mozilla = %(rpm -q mozilla --queryformat %{VERSION})
%endif
%endif
Provides: pyphany
Obsoletes: pyphany

%description
Epiphany is a GNOME web browser based on the mozilla
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
%if %{build_with_webkit}
Requires: webkitgtk-devel
Requires: icu-devel
Requires: sqlite3-devel
%else
%if %build_with_xulrunner
Requires: xulrunner-devel-unstable >= %xulrunner
%else
%if %{build_with_firefox}
Requires: mozilla-firefox-devel
%else
Requires: mozilla-devel
%endif
%endif
%endif


%description devel
This contains the C headers required for developing with Epiphany.

%prep
%setup -q
%patch1 -p1 -b .defaults
%patch6 -p1 -b .defaultbookmarks
%patch9 -p1 -b .urpmi

%build

aclocal -Im4
automake
autoconf
%configure2_5x --with-distributor-name=Mandriva \
%if %{build_with_webkit}
--with-engine=webkit \
%else
--with-engine=mozilla \
%if %build_with_xulrunner
--with-mozilla=libxul-embedding \
%else
%if %{build_with_firefox}
%if %mdkversion >= 200710
--with-mozilla=firefox \
%else
--with-mozilla=mozilla-firefox \
%endif
%endif
%endif
%endif
%if %{with_python}
--enable-python \
%endif
--disable-filepicker --disable-scrollkeeper --enable-spell-checker

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

%clean
rm -rf $RPM_BUILD_ROOT

%define schemas epiphany epiphany-lockdown epiphany-fonts epiphany-pango

%post
%if %mdkversion < 200900
%{update_scrollkeeper}
%post_install_gconf_schemas %{schemas}
%endif
if [ "$1" = "2" ]; then
update-alternatives --remove webclient-gnome %{_bindir}/epiphany
update-alternatives --remove webclient-kde %{_bindir}/epiphany
fi
%if %mdkversion < 200900
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%{update_menus}
%endif

%preun
%preun_uninstall_gconf_schemas %{schemas}

%if %mdkversion < 200900
%postun
%{clean_scrollkeeper}
%{clean_menus}
%clean_icon_cache hicolor
%endif

%files -f %{name}-2.0.lang
%defattr(-,root,root,-)
%doc COPYING.README COPYING README TODO NEWS ChangeLog
%{_sysconfdir}/gconf/schemas/epiphany.schemas
%{_sysconfdir}/gconf/schemas/epiphany-fonts.schemas
%{_sysconfdir}/gconf/schemas/epiphany-pango.schemas
%{_sysconfdir}/gconf/schemas/epiphany-lockdown.schemas
%{_bindir}/*
%{_mandir}/man1/%name.1*
%{_datadir}/applications/*
%{_datadir}/epiphany
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/HighContrastLargePrint/*/apps/*
%{_datadir}/icons/HighContrastLargePrintInverse/*/apps/*
%{_datadir}/icons/LowContrastLargePrint/*/apps/*
%dir %{_datadir}/omf/epiphany
%{_datadir}/omf/epiphany/epiphany-C.omf
%if %{with_python}
%{_datadir}/pygtk/2.0/defs/*
%endif
%{_datadir}/dbus-1/services/org.gnome.Epiphany.service
%_liconsdir/*.png
%_iconsdir/*.png
%_miconsdir/*.png
%_datadir/pixmaps/*.png
%dir %_libdir/epiphany
%dir %_libdir/epiphany/%dirver/
%dir %_libdir/epiphany/%dirver/extensions
%if ! %{build_with_webkit}
%_libdir/epiphany/%dirver/plugins
%endif

%files devel
%defattr(-,root,root,-)
%_includedir/*
%_libdir/pkgconfig/*
%_datadir/gtk-doc/html/epiphany
%_datadir/aclocal/*.m4
