%define		beta 1

Summary:	GTK ASTerisk MANager
Name:		gastman
Epoch:		1
Version:	1.0
Release:	0.%{?beta:RC%{beta}}.5
Group:		System/Configuration/Networking
License:	GPLv2+
URL:		http://www.asterisk.org
Source0:	%{name}-%{version}%{?beta:-RC%{beta}}.tar.gz
Patch0:		gastman-20040803-mdk.diff
Patch1:		gastman-1.0-gold.patch
BuildRequires:	gtk+2-devel
BuildRequires:	imagemagick
BuildRequires:  db-devel
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
GTK ASTerisk MANager is a administration tool for asterisk.

%prep

%setup -q -n %{name}-%{version}%{?beta:-RC%{beta}}
%patch0 -p0
%patch1 -p0

%build

%make CC="gcc %{?ldflags}"

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_datadir}/%{name}/icons
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}

install -m0755 gastman %{buildroot}%{_sbindir}/
install -m0644 art/*.xpm %{buildroot}%{_datadir}/%{name}/icons/

# Mandriva Icons
convert -size 48x48 art/phone2.xpm %{buildroot}%{_liconsdir}/%{name}.png
convert -size 32x32 art/phone2.xpm %{buildroot}%{_iconsdir}/%{name}.png
convert -size 16x16 art/phone2.xpm %{buildroot}%{_miconsdir}/%{name}.png

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=%{summary}
Exec=%{_sbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Settings;Network;
EOF

%if %mdkversion < 200900
%post
%update_menus
%update_desktop_database
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_desktop_database
%endif

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%{_sbindir}/*
%{_datadir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*.desktop


%changelog
* Tue May 08 2012 Crispin Boylan <crisb@mandriva.org> 1:1.0-0.RC1.5
+ Revision: 797566
- Rebuild

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - rebuild against db 5.1.25

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-0.RC1.3mdv2011.0
+ Revision: 610818
- rebuild

* Sat Jan 30 2010 Funda Wang <fwang@mandriva.org> 1:1.0-0.RC1.2mdv2010.1
+ Revision: 498559
- add epoch
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Lonyai Gergely <aleph@mandriva.org>
    - Update: 1.0-RC1

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 20050401-6mdv2009.0
+ Revision: 245657
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Dec 14 2007 Funda Wang <fwang@mandriva.org> 20050401-4mdv2008.1
+ Revision: 119611
- drop old menu

  + Thierry Vignaud <tv@mandriva.org>
    - s/Mandrake/Mandriva/

