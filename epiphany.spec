%define _disable_ld_no_undefined 1
%define _disable_rebuild_configure 1

%define url_ver %(echo %{version}|cut -d. -f1,2)
#define api	3.18

Summary:	GNOME web browser based on the webkit rendering engine
Name:		epiphany
Version:	3.30.2
Release:	1
License:	GPLv2+ and GFDL
Group:		Networking/WWW
Url:		http://www.gnome.org/projects/epiphany/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/epiphany/%{url_ver}/%{name}-%{version}.tar.xz
# (fc) 0.9.2-2mdk fix defaults settings
#Patch1:		epiphany-3.2.1-defaults.patch
# (fc) 1.4.6-2mdk default bookmarks
#Patch2:		epiphany-defaultbookmarks.patch
# (fc) 1.8.5-4mdk set urpmi and bundles mimetypes as safe (Mdk bug #21892)
Patch3:		epiphany-1.8.5-urpmi.patch
# indexhtml
#Patch4:		epiphany-3.4.1-default-indexhtml.patch

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
BuildRequires:	pkgconfig(libsoup-gnome-2.4)
BuildRequires:	pkgconfig(libwnck-3.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(webkit2gtk-4.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	meson
BuildRequires:	pkgconfig(libsecret-1)

#gw for the index themes
Requires:	dbus-x11
Requires:	enchant
Requires:	gnome-themes
Requires:	gnome-doc-utils >= 0.3.2
Requires:	indexhtml
Requires:	iso-codes

%description
Epiphany is a GNOME web browser based on the webkit rendering engine.
The name meaning: "An intuitive grasp of reality through something
(as an event) usually simple and striking"

%prep
%setup -q
%autopatch -p1

%build
%meson -Ddistributor_name=%{_vendor}
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
%doc COPYING README TODO NEWS
%{_bindir}/*
%dir %{_libdir}/epiphany
%dir %{_libdir}/epiphany/%{api}/
%dir %{_libdir}/epiphany/%{api}/web-extensions
%{_libdir}/epiphany/%{api}/web-extensions/libephywebextension.so
%{_libexecdir}/epiphany-search-provider
%{_datadir}/appdata/*
%{_datadir}/applications/*
%{_datadir}/dbus-1/services/org.gnome.Epiphany.service
%{_datadir}/epiphany
%{_datadir}/GConf/gsettings/epiphany.convert
%{_datadir}/glib-2.0/schemas/org.gnome.Epiphany.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.epiphany.gschema.xml
%{_datadir}/gnome-shell/search-providers/epiphany-search-provider.ini
%{_mandir}/man1/%{name}.1*
