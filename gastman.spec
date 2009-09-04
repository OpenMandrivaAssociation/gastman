%define		beta 1

Summary:	GTK ASTerisk MANager
Name:		gastman
Version:	1.0
Release:	%mkrel 0.%{?beta:RC%{beta}}.2
Group:		System/Configuration/Networking
License:	GPLv2+
URL:		http://www.asterisk.org
Source0:	%{name}-%{version}%{?beta:-RC%{beta}}.tar.gz
Patch0:		gastman-20040803-mdk.diff
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

%build

%make

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
