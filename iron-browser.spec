Summary:	SRWare Iron: The Browser of the future
Name:		iron-browser
Version:	31.0.700.0
Release:	0.1
License:	BSD, LGPL v2+ (ffmpeg)
Group:		X11/Applications/Networking
Source0:	http://www.srware.net/downloads/iron-linux.tar.gz
# Source0-md5:	4592966535ffbedb7404c935f9abd9a6
Source1:	http://www.srware.net/downloads/iron-linux-64.tar.gz
# Source1-md5:	655d52dfd5612a7aecaa6f0c24174546
Source2:	find-lang.sh
URL:		http://www.srware.net/en/software_srware_iron.php
Requires:	browser-plugins >= 2.0
Requires:	libvpx >= 0.9.5-2
Requires:	xdg-utils >= 1.0.2-4
Provides:	wwwbrowser
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		find_lang 	sh find-lang.sh %{buildroot}

%description
SRWare Iron: The browser of the future - based on the free Sourcecode
"Chromium" - without any problems at privacy and security.

%package l10n
Summary:	SRWare Iron: language packages
Group:		I18n
Requires:	%{name} = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description l10n
This package contains language packages for 50 languages:

ar, bg, bn, ca, cs, da, de, el, en-GB, es-419, es, et, fi, fil, fr,
gu, he, hi, hr, hu, id, it, ja, kn, ko, lt, lv, ml, mr, nb, nl, or,
pl, pt-BR, pt-PT, ro, ru, sk, sl, sr, sv, ta, te, th, tr, uk, vi,
zh-CN, zh-TW

%prep
%ifarch %{ix86}
%setup -qT -b 0 -n iron-linux
%endif
%ifarch %{x8664}
%setup -qT -b 1 -n iron64
%endif

set -- *
install -d chrome
mv "$@" chrome

%{__sed} -e 's,@localedir@,%{_datadir}/%{name},' %{SOURCE2} > find-lang.sh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_desktopdir},%{_pixmapsdir}} \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/plugins \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/{locales,resources}

cp -a chrome/* $RPM_BUILD_ROOT%{_libdir}/%{name}
mv $RPM_BUILD_ROOT{%{_libdir}/%{name}/product_logo_48.png,%{_pixmapsdir}/%{name}.png}
mv $RPM_BUILD_ROOT{%{_libdir}/%{name}/locales,%{_datadir}/%{name}}
mv $RPM_BUILD_ROOT{%{_libdir}/%{name}/resources,%{_datadir}/%{name}}
ln -s %{_datadir}/%{name}/locales $RPM_BUILD_ROOT%{_libdir}/%{name}
ln -s %{_datadir}/%{name}/resources $RPM_BUILD_ROOT%{_libdir}/%{name}

# find locales
%find_lang %{name}.lang
# always package en-US (in main package)
%{__sed} -i -e '/en-US.pak/d' %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
#%attr(755,root,root) %{_bindir}/%{name}
%{_pixmapsdir}/%{name}.png
#%{_desktopdir}/*.desktop
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.pak
%{_libdir}/%{name}/resources
%{_libdir}/%{name}/locales
%dir %{_libdir}/%{name}/extensions
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/iron
%attr(755,root,root) %{_libdir}/%{name}/chrome-wrapper
# These unique permissions are intentional and necessary for the sandboxing
%attr(4555,root,root) %{_libdir}/%{name}/chrome_sandbox

%attr(755,root,root) %{_libdir}/%{name}/libavcodec.so.52
%attr(755,root,root) %{_libdir}/%{name}/libavformat.so.52
%attr(755,root,root) %{_libdir}/%{name}/libavutil.so.50
%attr(755,root,root) %{_libdir}/%{name}/libffmpegsumo.so

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/resources
%dir %{_datadir}/%{name}/locales
%{_datadir}/%{name}/locales/en-US.pak

%files l10n -f %{name}.lang
%defattr(644,root,root,755)
