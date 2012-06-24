%define		_modname	http
%define		_fmodname	pecl_http
%define		_status		stable
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	%{_modname} - extended HTTP support
Summary(pl):	%{_modname} - rozszerzona obs�uga protoko�u HTTP
Name:		php-pecl-%{_modname}
Version:	1.3.3
Release:	1
License:	BSD
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_fmodname}-%{version}.tgz
# Source0-md5:	96c16435936eab288d5fdd5750e3f863
URL:		http://pecl.php.net/package/pecl_http/
BuildRequires:	curl-devel >= 7.12.3
BuildRequires:	openssl-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.322
BuildRequires:	zlib-devel >= 1.2.0.4
Requires:	%{_sysconfdir}/conf.d
%{?requires_php_extension}
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This HTTP extension aims to provide a convenient and powerful set of
functionality for one of PHPs major applications.

It eases handling of HTTP urls, dates, redirects, headers and
messages, provides means for negotiation of clients preferred language
and charset, as well as a convenient way to send any arbitrary data
with caching and resuming capabilities.

It provides powerful request functionality, if built with CURL
support. Parallel requests are available for PHP 5 and greater.

Currently implemented features include:
- Building absolute URIs
- RFC compliant HTTP redirects
- RFC compliant HTTP date handling
- Parsing of HTTP headers and messages
- Caching by "Last-Modified" and/or ETag (with 'on the fly' option for
  ETag generation from buffered output)
- Sending data/files/streams with (multiple) ranges support
- Negotiating user preferred language/charset
- Convenient request functions to HEAD/GET/POST if libcurl is
  available
- HTTP auth hooks (Basic)
- PHP5 classes: HttpUtil, HttpResponse, HttpRequest, HttpRequestPool,
  HttpMessage

In PECL status of this extension is: %{_status}.

%description -l pl
To rozszerzenie HTTP ma na celu dostarczenie wygodnego i pot�nego
zestawu funkcjonalno�ci do jednego z najwa�niejszych zastosowa� PHP.

U�atwia obs�ug� adres�w HTTP, dat, przekierowa�, nag��wk�w i
wiadmo�ci, dostarcza spos�b do negocjacji preferowanego j�zyka i
strony kodowej klienta, jak r�wnie� wygodnego sposobu wysy�ania
dowolnego rodzaju danych z mo�liwo�ci� keszowania oraz wznawiania
transfer�w.

Rozszerzenie dostarcza pot�ne mo�liwo�ci zapyta�, je�li zbudowane
jest ze wsparciem dla CURL. R�wnoleg�e zapytania s� dost�pne od wersji
PHP 5.

Aktualnie zaimplementowane mo�liwo�ci to mi�dzy innymi:
- tworzenie bezwzgl�dnych URI
- zgodne z RFC przekierowania HTTP
- zgodna z RFC obs�uga daty HTTP
- przetwarzanie nag��wk�w i wiadomo�ci HTTP
- buforowanie z u�yciem "Last-Modified" i/lub ETag�w (z opcj�
  generowania "w locie" ETag�w z buforowanego wyj�cia)
- wysy�anie danych/plik�w/strumieni z obs�ug� (wielu) przedzia��w
- negocjacja preferowanego przez u�ytkownika j�zyka/zestawu znak�w
- wygodne funkcje do ��da� HEAD/GET/POST je�li dost�pna jest libcurl
- wywo�ania HTTP auth (Basic)
- klasy PHP5: HttpUtil, HttpResponse, HttpRequest, HttpRequestPool,
  HttpMessage

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
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_fmodname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}/%{_modname}.so
cat << 'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
        [ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
        [ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_fmodname}-%{version}/{KnownIssues.txt,docs}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
