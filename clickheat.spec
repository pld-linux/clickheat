# TODO
# - frontend package
# - admin package
%define		php_min_version 5.0.0
Summary:	ClickHeat | Clicks heatmap
Name:		clickheat
Version:	1.12
Release:	0.12
License:	GPL v2
Group:		Applications/WWW
Source0:	http://downloads.sourceforge.net/clickheat/%{name}-%{version}.zip
# Source0-md5:	5a4a057a55c904782facad0add684e69
Source1:	apache.conf
Source2:	lighttpd.conf
Source3:	config.php
Patch0:		paths.patch
Patch1:		languages.patch
Patch2:		js-scoping.patch
URL:		http://www.labsmedia.com/clickheat/
BuildRequires:	js
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	yuicompressor
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-gd
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

# bad depsolver
%define		_noautopear	pear

# exclude optional php dependencies
%define		_noautophp	php-mysql

# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

%description
ClickHeat is a visual heatmap of clicks on a HTML page, showing hot
and cold click zones.

%prep
%setup -qc
mv %{name}/* .
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

# to satisfy deps
%{__sed} -i -e '1s,#!/usr/bin/php5-cgi -q,#!/usr/bin/php,' scripts/compressJs.php

# simplify packaging
install -d doc
mv INSTALL LICENSE LISEZMOI README VERSION doc
%{__rm} languages/__readme.txt images/flags/_flags.txt

%{__rm} {cache,config,logs}/.htaccess
rmdir cache config logs

%build
# compress .js
yuicompressor --charset UTF-8 js/clickheat-original.js -o js/clickheat.js
js -C -f js/clickheat.js

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},/var/{cache,log}/%{name}}

cp -a . $RPM_BUILD_ROOT%{_appdir}
ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/config
rm -rf $RPM_BUILD_ROOT%{_appdir}/{doc,examples,scripts}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

rm $RPM_BUILD_ROOT%{_appdir}/js/clickheat-original.js

process_languages() {
	echo "%dir %{_appdir}/languages"
	echo "%dir %{_appdir}/images/flags"
	for f in languages/*.php; do
		l=${f##*/} l=${l%*.php}
		ll="%lang($l)"
		if [ $l = en ]; then
			ll=
		fi
		echo "$ll %{_appdir}/languages/$l.php"
		echo "$ll %{_appdir}/images/flags/$l.png"
	done
}
process_languages > %{name}.lang

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -a $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc doc/* scripts
%dir %attr(770,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/*.html
%{_appdir}/classes
%{_appdir}/config
%dir %{_appdir}/images
%{_appdir}/images/*.png
%{_appdir}/js
%{_appdir}/styles
%{_examplesdir}/%{name}-%{version}
%dir %attr(775,root,http) /var/cache/%{name}
%dir %attr(775,root,http) /var/log/%{name}
