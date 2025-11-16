Summary:	The uv build backend
Summary(pl.UTF-8):	Backend budowania uv
Name:		python3-uv-build
Version:	0.9.9
Release:	1
License:	MIT or Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/uv-build/
Source0:	https://files.pythonhosted.org/packages/source/u/uv-build/uv_build-%{version}.tar.gz
# Source0-md5:	9953b0e4c69a85b79a5e5416ec0ab2de
%define	reqwest_middleware_ver	7650ed76215a962a96d94a79be71c27bffde7ab2
Source1:	https://github.com/astral-sh/reqwest-middleware/archive/%{reqwest_middleware_ver}/reqwest-middleware-%{reqwest_middleware_ver}.tar.gz
# Source1-md5:	41f840de9fee54a629a6e4cea269d007
%define	pubgrub_ver	d8efd77673c9a90792da9da31b6c0da7ea8a324b
Source2:	https://github.com/astral-sh/pubgrub/archive/%{pubgrub_ver}/pubgrub-%{pubgrub_ver}.tar.gz
# Source2-md5:	c28f6081bd3c3b9cd8a7732ad902bc02
# after placing Source1 and Source2 contents into crates:
# cargo vendor-filterer --platform='*-unknown-linux-*' --tier=2 $(for f in crates/uv-*/Cargo.toml ; do echo -s $f ; done | grep -v reqwest-tracing)
# tar cJf uv_build-%{version}-vendor.tar.xz vendor Cargo.lock
Source3:	uv_build-%{version}-vendor.tar.xz
# Source3-md5:	31a9d27147b2350a3414e0432acd858d
URL:		https://pypi.org/project/uv-build/
BuildRequires:	bzip2-devel
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
%setup -q -n uv_build-%{version} -a1 -a2 -a3

%{__mv} reqwest-middleware-%{reqwest_middleware_ver}/{reqwest-middleware,reqwest-retry,reqwest-tracing} crates
%{__mv} pubgrub-%{pubgrub_ver}/version-ranges crates

%{__sed} -i -e '/^reqwest-middleware / s!git = "https://github.com/astral-sh/reqwest-middleware", rev = "7650ed76215a962a96d94a79be71c27bffde7ab2"!path = "crates/reqwest-middleware"!' Cargo.toml
%{__sed} -i -e '/^reqwest-retry / s!git = "https://github.com/astral-sh/reqwest-middleware", rev = "7650ed76215a962a96d94a79be71c27bffde7ab2"!path = "crates/reqwest-retry"!' Cargo.toml
%{__sed} -i -e '/^version-ranges / s!git = "https://github.com/astral-sh/pubgrub", rev = "d8efd77673c9a90792da9da31b6c0da7ea8a324b"!path = "crates/version-ranges"!' Cargo.toml

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
