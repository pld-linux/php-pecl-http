%define		_modname	http
%define		_fmodname	pecl_http
%define		_status		alpha

Summary:	%{_modname} - extended HTTP support
Summary(pl):	%{_modname} - rozszerzone wsparcie protoko³u HTTP
Name:		php-pecl-%{_modname}
Version:	0.5.0
Release:	1
License:	PHP 3.0
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_fmodname}-%{version}.tgz
# Source0-md5:	5f66c8c2ec72005b4e81e58ab594e489
URL:		http://pecl.php.net/package/pecl_http/
BuildRequires:	libtool
BuildRequires:	php-devel >= 3:5.0.0
Requires:	php-common >= 3:5.0.0
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
Currently implemented features:
===============================

- Building absolute URIs
- RFC compliant HTTP redirects
- RFC compliant HTTP date handling
- Parsing of HTTP headers and responses
- Caching by "Last-Modified" and/or ETag (with 'on the fly' option for
  ETag generation from buffered output)
- Sending data/files/streams with (multiple) ranges support
- Negotiating user preferred language/charset
- Convenient request functions to HEAD/GET/POST if libcurl is available
- HTTP auth hooks (Basic)
- HTTPi, HTTPi_Response and HTTPi_Request (with libcurl) classes

In PECL status of this extension is: %{_status}.

#%description -l pl
#
#To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_fmodname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_fmodname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}/%{_modname}.so

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php-cgi.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php-cgi.ini
fi

%files
%defattr(644,root,root,755)
%doc %{_fmodname}-%{version}/{docs,EXPERIMENTAL}
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
