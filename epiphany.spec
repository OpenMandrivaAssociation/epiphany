%define api 3.4

Summary: GNOME web browser based on the webkit rendering engine
Name: epiphany
Version: 3.4.2
Release: 1
License: GPLv2+ and GFDL
Group: Networking/WWW
URL: http://www.gnome.org/projects/epiphany/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/epiphany/%{name}-%{version}.tar.xz
# (fc) 0.9.2-2mdk fix defaults settings
Patch1:	epiphany-3.2.1-defaults.patch
# (fc) 1.4.6-2mdk default bookmarks
Patch2: epiphany-defaultbookmarks.patch
# (fc) 1.8.5-4mdk set urpmi and bundles mimetypes as safe (Mdk bug #21892)
Patch3: epiphany-1.8.5-urpmi.patch
# indexhtml
Patch4:	epiphany-3.4.1-default-indexhtml.patch

BuildRequires:	desktop-file-utils
BuildRequires:	gnome-common
BuildRequires:	gtk-doc
BuildRequires:	imagemagick
BuildRequires:	intltool
BuildRequires:	rootcerts
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	pkgconfig(avahi-gobject)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libsoup-gnome-2.4)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(seed)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(webkitgtk-3.0)
BuildRequires:	pkgconfig(x11)

#gw for the index themes
Requires: dbus-x11
Requires: enchant
Requires: gnome-themes
Requires: gnome-doc-utils >= 0.3.2
Requires: indexhtml
Requires: iso-codes

%description
Epiphany is a GNOME web browser based on the webkit rendering engine.
The name meaning: "An intuitive grasp of reality through something 
(as an event) usually simple and striking"

%package devel
Group: Development/C
Summary: Header files for developing with Epiphany

%description devel
This contains the C headers required for developing with Epiphany.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--with-distributor-name=%{vendor} \
	--disable-scrollkeeper

%make LIBS='-lgmodule-2.0'

%install
%makeinstall_std
%find_lang %{name} --with-gnome --all-name

mkdir -p  %{buildroot}%{_libdir}/epiphany/%{api}/extensions

#gw these are useless
rm -f %{buildroot}%{_datadir}/icons/LowContrastLargePrint/*/apps/*

%post
if [ "$1" = "2" ]; then
	update-alternatives --remove webclient-gnome %{_bindir}/epiphany
	update-alternatives --remove webclient-kde %{_bindir}/epiphany
fi

%files -f %{name}.lang
%doc COPYING.README COPYING README TODO NEWS
%{_bindir}/*
%dir %{_libdir}/epiphany
%dir %{_libdir}/epiphany/%{api}/
%dir %{_libdir}/epiphany/%{api}/extensions
%{_libdir}/girepository-1.0/Epiphany-%{api}.typelib
%{_datadir}/applications/*
%{_datadir}/dbus-1/services/org.gnome.Epiphany.service
%{_datadir}/epiphany
%{_datadir}/GConf/gsettings/epiphany.convert
%{_datadir}/glib-2.0/schemas/org.gnome.Epiphany.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.epiphany.gschema.xml
%{_mandir}/man1/%{name}.1*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/epiphany
%{_datadir}/aclocal/*.m4
%{_datadir}/gir-1.0/Epiphany-%{api}.gir
