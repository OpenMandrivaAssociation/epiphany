%define _disable_ld_no_undefined 1
%define _disable_rebuild_configure 1

%define url_ver %(echo %{version}|cut -d. -f1,2)

Summary:	GNOME web browser based on the webkit rendering engine
Name:		epiphany
Version:	43.0
Release:	1
License:	GPLv2+ and GFDL
Group:		Networking/WWW
Url:		http://www.gnome.org/projects/epiphany/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/epiphany/%{url_ver}/%{name}-%{version}.tar.xz


BuildRequires:  appstream-util
BuildRequires:  cmake
BuildRequires:	desktop-file-utils
BuildRequires:	gnome-common
BuildRequires:	gtk-doc
BuildRequires:	imagemagick
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	rootcerts
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	pkgconfig(avahi-gobject)
BuildRequires:	pkgconfig(gcr-3)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:  pkgconfig(libportal)
BuildRequires:	pkgconfig(libsoup-3.0)
BuildRequires:	pkgconfig(libwnck-3.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(webkit2gtk-4.1)
BuildRequires:	pkgconfig(x11)
BuildRequires:	meson
BuildRequires:	pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libdazzle-1.0)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libhandy-1)
BuildRequires:  pkgconfig(hogweed)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  gmp-devel

#gw for the index themes
Requires:	dbus-x11
Requires:	enchant
Requires:	gnome-themes
Requires:	gnome-doc-utils >= 0.3.2
Requires:	indexhtml
Requires:	iso-codes
# From 3.34.4 xdg-dbus-proxy is required. If not installed then epiphany crashing at launch.
Requires: xdg-dbus-proxy

%description
Epiphany is a GNOME web browser based on the webkit rendering engine.
The name meaning: "An intuitive grasp of reality through something
(as an event) usually simple and striking"

%prep
%setup -q
%autopatch -p1

%build
#export CC=gcc
#export CXX=g++

%meson
%meson_build

%install
%meson_install
%find_lang %{name} --with-gnome

#gw these are useless
rm -f %{buildroot}%{_datadir}/icons/LowContrastLargePrint/*/apps/*
find %{buildroot} -name '*.la' -delete

%post
if [ "$1" = "2" ]; then
update-alternatives --remove webclient-gnome %{_bindir}/epiphany || :
update-alternatives --remove webclient-kde %{_bindir}/epiphany || :
fi

%files -f %{name}.lang
%doc README.md NEWS
%{_bindir}/*
%{_mandir}/man1/%{name}.1*
%{_datadir}/applications/org.gnome.Epiphany.desktop
%{_datadir}/%{name}/
%{_datadir}/dbus-1/services/org.gnome.Epiphany.SearchProvider.service
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/libephymain.so
%{_libdir}/%{name}/libephymisc.so
%{_libdir}/%{name}/libephysync.so
%{_libdir}/epiphany/web-process-extensions/libephywebprocessextension.so
%{_datadir}/glib-2.0/schemas/org.gnome.Epiphany.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.%{name}.gschema.xml
%{_datadir}/gnome-shell/search-providers/org.gnome.Epiphany.SearchProvider.ini
%{_datadir}/metainfo/org.gnome.Epiphany.appdata.xml
%{_datadir}/icons/hicolor/*/apps/org.gnome.Epiphany*
%{_libexecdir}/%{name}-search-provider
%{_libexecdir}/epiphany/ephy-profile-migrator
