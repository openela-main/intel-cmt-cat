%global libpqos_ver 6.0.1
%global desc %{expand: \
This package provides basic support for Intel Resource Director Technology
including, Cache Monitoring Technology (CMT), Memory Bandwidth Monitoring
(MBM), Cache Allocation Technology (CAT), Code and Data Prioritization
(CDP) and Memory Bandwidth Allocation (MBA).}

Name:		intel-cmt-cat
Version:	25.04
Release:	1%{?dist}
Summary:	Intel cache monitoring and allocation technology config tool

License:	BSD-3-Clause
URL: 		https://github.com/intel/intel-cmt-cat
Source: 	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz

ExclusiveArch:	x86_64

BuildRequires:	gcc
BuildRequires:	make

%description
%{desc}

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel %{desc}

Development files.

%prep
%autosetup -p1 -n %{name}-%{version}

# lib: honor DESTDIR and drop ldconfig
sed -i 's|\$(LIB_INSTALL_DIR)|$(DESTDIR)$(LIB_INSTALL_DIR)|g' lib/Makefile
sed -i 's|\$(HDR_DIR)|$(DESTDIR)$(HDR_DIR)|g' lib/Makefile
sed -i '/^[[:space:]]*ldconfig[[:space:]]*$/d' lib/Makefile

# pqos: honor DESTDIR for binaries and man pages
sed -i 's|\$(PREFIX)/bin|$(DESTDIR)$(PREFIX)/bin|g' pqos/Makefile
sed -i 's|^MAN_DIR *=.*|MAN_DIR = $(DESTDIR)%{_mandir}/man8|' pqos/Makefile

# rdtset: honor DESTDIR for binaries and man pages
sed -i 's|\$(PREFIX)/bin|$(DESTDIR)$(PREFIX)/bin|g' rdtset/Makefile
sed -i 's|^MAN_DIR *=.*|MAN_DIR = $(DESTDIR)%{_mandir}/man8|' rdtset/Makefile

# membw: honor DESTDIR for binaries and man pages
sed -i 's|\$(PREFIX)/bin|$(DESTDIR)$(PREFIX)/bin|g' tools/membw/Makefile
sed -i 's|^MAN_DIR *=.*|MAN_DIR = $(DESTDIR)%{_mandir}/man8|' tools/membw/Makefile

# Ensure CFLAGS/LDFLAGS are augmented (+=) instead of overwritten (=)
for mf in $(find . -name Makefile); do
    sed -i 's/^\(CFLAGS\)[[:space:]]*=/\1 +=/' "$mf"
    sed -i 's/^\(LDFLAGS\)[[:space:]]*=/\1 +=/' "$mf"
done

%build
%make_build

%install
%make_install PREFIX=%{_prefix} LIB_INSTALL_DIR=%{_libdir} HDR_DIR=%{_includedir} MANDIR=%{_mandir}

# Relocate admin tools from bin → sbin
for tool in pqos pqos-msr pqos-os rdtset; do
    install -D -m 0755 %{buildroot}%{_bindir}/$tool %{buildroot}%{_sbindir}/$tool
    rm -f %{buildroot}%{_bindir}/$tool
done

%ldconfig_scriptlets

%files
%license LICENSE
%doc ChangeLog README.md
%{_bindir}/membw
%{_sbindir}/pqos
%{_sbindir}/pqos-msr
%{_sbindir}/pqos-os
%{_sbindir}/rdtset
%{_libdir}/libpqos.so.6
%{_libdir}/libpqos.so.%{libpqos_ver}
%{_mandir}/man8/membw.8*
%{_mandir}/man8/pqos.8*
%{_mandir}/man8/pqos-msr.8*
%{_mandir}/man8/pqos-os.8*
%{_mandir}/man8/rdtset.8*

%files -n %{name}-devel
%{_includedir}/pqos.h
%{_libdir}/libpqos.so

%changelog
* Mon Oct 13 2025 Tony Camuso <tcamuso@redhat.com> - 25.04-1
Clean up install paths, drop obsolete patches, and improve flag injection
handling
- Replaced hard-coded install paths in Makefiles with sed-based DESTDIR
  fixes for lib, pqos, rdtset, and membw
  - Using sed during %prep is more robust and version-agnostic than patching,
    which requires rebasing each release
- Relocated admin tools (pqos*, rdtset) from /usr/bin to /usr/sbin for FHS
  compliance
  - These tools require root and interact with system-level cache controls
- Updated %files to match SONAME bump (libpqos.so.5 -> libpqos.so.6) introduced
  upstream
- Dropped patches 0001, 0002, 0004, 0005
  - 0001/0002 replaced by sed
  - 0004/0005 merged upstream
- Replaced patch 0003 (CFLAGS/LDFLAGS override) with sed to convert assignments
  to +=
  - Ensures compatibility with distro-injected flags (e.g. %{optflags},
    hardening) without carrying a version-specific patch
  Resolves: RHEL-118205

* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 23.11-6
- Bump release for October 2024 mass rebuild:
  Resolves: RHEL-64018

* Fri Aug 23 2024 Eugene Syromiatnikov <esyr@redhat.com> - 23.11-5
- Address issues reported by SAST (RHEL-40017)

* Mon Jun 24 2024 Troy Dawson <tdawson@redhat.com> - 23.11-4
- Bump release for June 2024 mass rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 13 2023 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 23.11-1
- Update to 23.11

* Thu Aug 31 2023 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 23.08-1
- Update to 23.08

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Mar 06 2023 Raghavan Kanagaraj <raghavan.kanagaraj@intel.com> - 4.5.0-1
- New release 4.5.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 12 2022 Marcel cornu <marcel.d.cornu@intel.com> - 4.4.1-1
- New release 4.4.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Mar 1 2022 Khawar Abbasi <khawar.abbasi@intel.com> - 4.3.0-1
- New release 4.3.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 18 2020 Khawar Abbasi <khawar.abbasi@intel.com> - 4.1.0-1
- New release 4.1.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Khawar Abbasi <khawar.abbasi@intel.com> - 4.0.0-1
- New release 4.0.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 30 2019 Marcel cornu <marcel.d.cornu@intel.com> - 3.1.1-1
- New release 3.1.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 27 2019 Marcel cornu <marcel.d.cornu@intel.com> - 3.0.1-1
- New release 3.0.1

* Mon Feb 18 2019 Marcel cornu <marcel.d.cornu@intel.com> - 3.0.0-1
- New release 3.0.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 16 2018 Marcel cornu <marcel.d.cornu@intel.com>, Michal Aleksinski <michalx.aleksinski@intel.com> 2.1.0-1
- New release 2.1.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Marcel cornu <marcel.d.cornu@intel.com>, Michal Aleksinski <michalx.aleksinski@intel.com> - 2.0.0-1
- New release 2.0.0

* Thu Mar 08 2018 Marcel cornu <marcel.d.cornu@intel.com>, Michal Aleksinski <michalx.aleksinski@intel.com> - 1.2.0-3
- Updated spec file with BuildRequires tag

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 29 2017 Marcel Cornu <marcel.d.cornu@intel.com>, Wojciech Andralojc <wojciechx.andralojc@intel.com> 1.2.0-1
- New release 1.2.0

* Thu Aug 3 2017 Aaron Hetherington <aaron.hetherington@intel.com>, Marcel Cornu <marcel.d.cornu@intel.com> 1.1.0-1
- New release 1.1.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 21 2017 Aaron Hetherington <aaron.hetherington@intel.com>, Marcel Cornu <marcel.d.cornu@intel.com> 1.0.1-1
- Spec file bug fixes

* Wed Jun 07 2017 Aaron Hetherington <aaron.hetherington@intel.com>, Marcel Cornu <marcel.d.cornu@intel.com> 1.0.1-1
- new release
- bug fixes

* Fri May 19 2017 Aaron Hetherington <aaron.hetherington@intel.com>, Michal Aleksinski <michalx.aleksinski@intel.com> 1.0.0-1
- new release

* Tue Feb 14 2017 Aaron Hetherington <aaron.hetherington@intel.com> 0.1.5-1
- new release

* Mon Oct 17 2016 Aaron Hetherington <aaron.hetherington@intel.com> 0.1.5
- new release

* Tue Apr 19 2016 Tomasz Kantecki <tomasz.kantecki@intel.com> 0.1.4-3
- global typo fix
- small edits in the description

* Mon Apr 18 2016 Tomasz Kantecki <tomasz.kantecki@intel.com> 0.1.4-2
- LICENSE file added to the package

* Thu Apr 7 2016 Tomasz Kantecki <tomasz.kantecki@intel.com> 0.1.4-1
- initial version of the package
