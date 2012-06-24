%define		_modname	http
%define		_fmodname	pecl_http
%define		_status		alpha

Summary:	%{_modname} - extended HTTP support
Summary(pl):	%{_modname} - rozszerzona obs�uga protoko�u HTTP
Name:		php-pecl-%{_modname}
Version:	0.6.1
Release:	1
License:	PHP 3.0
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_fmodname}-%{version}.tgz
# Source0-md5:	ae01c5f10a66a969cf954e52fcc0ce11
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

%description -l pl
Aktualnie zaimplementowane mo�liwo�ci:
- tworzenie bezwzgl�dnych URI
- zgodne z RFC przekierowania HTTP
- zgodna z RFC obs�uga daty HTTP
- przetwarzanie nag��wk�w i odpowiedzi HTTP
- buforowanie z u�yciem "Last-Modified" i/lub ETag�w (z opcj�
  generowania "w locie" ETag�w z buforowanego wyj�cia)
- wysy�anie danych/plik�w/strumieni z obs�ug� (wielu) przedzia��w
- negocjacja preferowanego przez u�ytkownika j�zyka/zestawu znak�w
- wygodne funkcje do ��da� HEAD/GET/POST je�li dost�pna jest libcurl
- wywo�ania HTTP auth (Basic)
- klasy HTTPi, HTTPi_Response i HTTPi_Request (z u�yciem libcurl)

To rozszerzenie ma w PECL status: %{_status}.

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
