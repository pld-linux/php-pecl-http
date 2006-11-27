%define		_modname	http
%define		_fmodname	pecl_http
%define		_status		stable
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	%{_modname} - extended HTTP support
Summary(pl):	%{_modname} - rozszerzona obs³uga protoko³u HTTP
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
To rozszerzenie HTTP ma na celu dostarczenie wygodnego i potê¿nego
zestawu funkcjonalno¶ci do jednego z najwa¿niejszych zastosowañ PHP.

U³atwia obs³ugê adresów HTTP, dat, przekierowañ, nag³ówków i
wiadmo¶ci, dostarcza sposób do negocjacji preferowanego jêzyka i
strony kodowej klienta, jak równie¿ wygodnego sposobu wysy³ania
dowolnego rodzaju danych z mo¿liwo¶ci± keszowania oraz wznawiania
transferów.

Rozszerzenie dostarcza potê¿ne mo¿liwo¶ci zapytañ, je¶li zbudowane
jest ze wsparciem dla CURL. Równoleg³e zapytania s± dostêpne od wersji
PHP 5.

Aktualnie zaimplementowane mo¿liwo¶ci to miêdzy innymi:
- tworzenie bezwzglêdnych URI
- zgodne z RFC przekierowania HTTP
- zgodna z RFC obs³uga daty HTTP
- przetwarzanie nag³ówków i wiadomo¶ci HTTP
- buforowanie z u¿yciem "Last-Modified" i/lub ETagów (z opcjê
  generowania "w locie" ETagów z buforowanego wyj¶cia)
- wysy³anie danych/plików/strumieni z obs³ug± (wielu) przedzia³ów
- negocjacja preferowanego przez u¿ytkownika jêzyka/zestawu znaków
- wygodne funkcje do ¿±dañ HEAD/GET/POST je¶li dostêpna jest libcurl
- wywo³ania HTTP auth (Basic)
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
