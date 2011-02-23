# TODO
# - frontend package
# - admin package
Summary:	ClickHeat | Clicks heatmap
Name:		clickheat
Version:	1.11
Release:	0.1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://downloads.sourceforge.net/clickheat/%{name}-%{version}.zip
# Source0-md5:	0ad7c917045772ebcc004027b4858098
Source1:	apache.conf
Source2:	lighttpd.conf
URL:		http://www.labsmedia.com/clickheat/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
# see packages/webapps/webapps.README for description and complete listing
Requires:	php-gd
Requires:	webserver(access)
Requires:	webserver(alias)
#Requires:	webserver(auth)
#Requires:	webserver(cgi)
#Requires:	webserver(indexfile)
Requires:	webserver(php)
#Requires:	webserver(setenv)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
ClickHeat is a visual heatmap of clicks on a HTML page, showing hot
and cold click zones.

%prep
%setup -qn %{name}

# simplify packaging
install -d doc
mv INSTALL LICENSE LISEZMOI README VERSION doc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

cp -a . $RPM_BUILD_ROOT%{_appdir}
rm -rf $RPM_BUILD_ROOT%{_appdir}/doc
rm $RPM_BUILD_ROOT%{_appdir}/js/clickheat-original.js

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -a $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

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

%files
%defattr(644,root,root,755)
%doc doc/*
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}
