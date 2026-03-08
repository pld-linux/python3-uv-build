Summary:	The uv build backend
Summary(pl.UTF-8):	Backend budowania uv
Name:		python3-uv-build
Version:	0.10.9
Release:	1
License:	MIT or Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/uv-build/
Source0:	https://files.pythonhosted.org/packages/source/u/uv-build/uv_build-%{version}.tar.gz
# Source0-md5:	86069f8132db847033a1a1ab30c78ddf
# cargo vendor-filterer --platform='*-unknown-linux-*' --tier=2 $(for f in crates/uv-*/Cargo.toml ; do echo -s $f ; done)
# tar cJf uv_build-%{version}-vendor.tar.xz vendor Cargo.lock
Source1:	uv_build-%{version}-vendor.tar.xz
# Source1-md5:	1ef584e94438083e196b37170e7014ac
URL:		https://pypi.org/project/uv-build/
BuildRequires:	bzip2-devel
BuildRequires:	cargo
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-installer
BuildRequires:	python3-maturin >= 1.0
BuildRequires:	python3-maturin < 2
BuildRequires:	rust >= 1.89
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.050
BuildRequires:	sed >= 4.0
BuildRequires:	xz-devel
%{?rust_req}
Requires:	python3-modules >= 1:3.8
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package is a slimmed down version of uv containing only the build
backend.

%description -l pl.UTF-8
Ten pakiet to odchudzona wersja uv, zawierająca tylko backend
budowania.

%prep
%setup -q -n uv_build-%{version} -a1

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config.toml <<EOF
[source.crates-io]
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"
export CARGO_OFFLINE=true
export CARGO_TERM_VERBOSE=true
%ifarch x32
export CARGO_BUILD_TARGET=x86_64-unknown-linux-gnux32
export PKG_CONFIG_ALLOW_CROSS=1
%endif

%py3_build_pyproject

%install
rm -rf $RPM_BUILD_ROOT

export CARGO_HOME="$(pwd)/.cargo"
export CARGO_OFFLINE=true
export CARGO_TERM_VERBOSE=true
%ifarch x32
export CARGO_BUILD_TARGET=x86_64-unknown-linux-gnux32
export PKG_CONFIG_ALLOW_CROSS=1
%endif

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE-MIT README.md
%attr(755,root,root) %{_bindir}/uv-build
%dir %{py3_sitedir}/uv_build
%{py3_sitedir}/uv_build/*.py
%{py3_sitedir}/uv_build/py.typed
%{py3_sitedir}/uv_build/__pycache__
%{py3_sitedir}/uv_build-%{version}.dist-info
