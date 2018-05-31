%define debug_package %{nil}
Summary:  Prometheus nginx exporter
Name: prom-nginx-exporter
Version: %version
Release:  1
License: Not Applicable
Group: Development/Library
URL: http://www.infinitycloud.com
BuildRequires: golang
BuildRoot: %{_tmppath}/%{name}-root
Source0: %{name}-%{version}.tar.gz
Requires: supervisor

%define PkgSrcPath src/github.com/infinitytracking/%{name}

%description
This package contains the prometheus nginx exporter.

%prep
%setup -q

%build
#Create a src directory and move all project directories into it (excluding conf).
#Then set the current directory as GOPATH and enable vendoring experiment.
mkdir -p %{PkgSrcPath}
mv `find . -maxdepth 1 -type d ! -name src ! -name conf ! -name .` %{PkgSrcPath}
export GOPATH=`pwd`

#Use go install to build all project programs, but exclude the vendor directory.
go install -v $(go list ./... | grep -v %{name}/vendor/)

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# Install app files
install -d -m 755 $RPM_BUILD_ROOT/usr/sbin
install -m 755 bin/prom-nginx-exporter $RPM_BUILD_ROOT/usr/sbin/prom-nginx-exporter

# Install supervisord config files
install -d -m 755 $RPM_BUILD_ROOT/etc/supervisord.d
install -m 644 conf/prom-nginx-exporter.supervisord $RPM_BUILD_ROOT/etc/supervisord.d/prom-nginx-exporter.ini

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/supervisord.d/prom-nginx-exporter.ini
/usr/sbin/prom-nginx-exporter
