# Copyright (c) 2016-2020, Intel Corporation
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Intel Corporation nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

%global githubname   intel-cmt-cat
%global githubver    23.11

%if %{defined githubsubver}
%global githubfull   %{githubname}-%{githubver}.%{githubsubver}
%else
%global githubfull   %{githubname}-%{githubver}
%endif

# disable producing debuginfo for this package
%global debug_package %{nil}


Summary:            Provides command line interface to CMT, MBM, CAT, CDP and MBA technologies
Name:               %{githubname}
Release:            1%{?dist}
Version:            %{githubver}
License:            BSD-3-Clause
ExclusiveArch:      x86_64 i686 i586
%if %{defined githubsubver}
Source:             https://github.com/intel/%{githubname}/archive/%{githubname}-%{githubver}.%{githubsubver}.tar.gz
%else
Source:             https://github.com/intel/%{githubname}/archive/%{githubname}-%{githubver}.tar.gz
%endif

Patch0001:          0001-allow-debian-flags-to-be-added.patch

URL:                https://github.com/intel/%{githubname}
BuildRequires:      gcc, make

%description
This software package provides basic support for
Cache Monitoring Technology (CMT), Memory Bandwidth Monitoring (MBM),
Cache Allocation Technology (CAT), Memory Bandwidth Allocation (MBA),
and Code Data Prioratization (CDP).

CMT, MBM and CAT are configured using Model Specific Registers (MSRs)
to measure last level cache occupancy, set up the class of service masks and
manage the association of the cores/logical threads to a class of service.
The software executes in user space, and access to the MSRs is
obtained through a standard Linux* interface. The virtual file system
provides an interface to read and write the MSR registers but
it requires root privileges.

%package -n intel-cmt-cat-devel
Summary:            Library and sample code to use CMT, MBM, CAT, CDP and MBA technologies
License:            BSD
Requires:           intel-cmt-cat == %{version}
ExclusiveArch:      x86_64 i686 i586

%description -n intel-cmt-cat-devel
This software package provides basic support for
Cache Monitoring Technology (CMT), Memory Bandwidth Monitoring (MBM),
Cache Allocation Technology (CAT), Memory Bandwidth Allocation (MBA),
and Code Data Prioratization (CDP).
The package includes library, header file and sample code.

For additional information please refer to:
https://github.com/intel/%{githubname}

%prep
%autosetup -p1 -n %{githubfull}

%ldconfig_scriptlets

%build
# RHEL 9's baseline is HSW/HSX, which has neither AVX-512 nor CLWB
make %{?_smp_mflags} HAS_AVX512=0 HAS_CLWB=0

%install
# Not doing make install as it strips the symbols.
# Using files from the build directory.

# pqos-* and rdtest are in %{_sbin} in Fedora now, but they are in %{_bin}
# in RHEL 9 originally, so, preserving it
install -d %{buildroot}/%{_bindir}
install -s %{_builddir}/%{githubfull}/pqos/pqos %{buildroot}/%{_bindir}
install %{_builddir}/%{githubfull}/pqos/pqos-os %{buildroot}/%{_bindir}
install %{_builddir}/%{githubfull}/pqos/pqos-msr %{buildroot}/%{_bindir}
sed -i "1s/.*/\#!\/usr\/bin\/bash/" %{buildroot}/%{_bindir}/pqos-*

install -d %{buildroot}/%{_mandir}/man8
install -m 0644 %{_builddir}/%{githubfull}/pqos/pqos.8  %{buildroot}/%{_mandir}/man8
ln -sf pqos.8 %{buildroot}/%{_mandir}/man8/pqos-os.8
ln -sf pqos.8 %{buildroot}/%{_mandir}/man8/pqos-msr.8

install -d %{buildroot}/%{_bindir}
install -s %{_builddir}/%{githubfull}/rdtset/rdtset %{buildroot}/%{_bindir}

install -d %{buildroot}/%{_mandir}/man8
install -m 0644 %{_builddir}/%{githubfull}/rdtset/rdtset.8  %{buildroot}/%{_mandir}/man8

# membw is istalled in %{_bindir} in Fedora, but the man page
# is in the section 8
install -d %{buildroot}/%{_bindir}
install -s %{_builddir}/%{githubfull}/tools/membw/membw %{buildroot}/%{_bindir}

install -d %{buildroot}/%{_mandir}/man8
install -m 0644 %{_builddir}/%{githubfull}/tools/membw/membw.8  %{buildroot}/%{_mandir}/man8

install -d %{buildroot}/%{_licensedir}/%{name}
install -m 0644 %{_builddir}/%{githubfull}/LICENSE %{buildroot}/%{_licensedir}/%{name}

# Install the library
install -d %{buildroot}/%{_libdir}
install -s %{_builddir}/%{githubfull}/lib/libpqos.so.* %{buildroot}/%{_libdir}
cp -a %{_builddir}/%{githubfull}/lib/libpqos.so %{buildroot}/%{_libdir}
cp -a %{_builddir}/%{githubfull}/lib/libpqos.so.5 %{buildroot}/%{_libdir}

# Install the header file
install -d %{buildroot}/%{_includedir}
install -m 0644 %{_builddir}/%{githubfull}/lib/pqos.h %{buildroot}/%{_includedir}

# Install license and sample code
install -d %{buildroot}/%{_usrsrc}/%{githubfull}
install -m 0644 %{_builddir}/%{githubfull}/LICENSE %{buildroot}/%{_usrsrc}/%{githubfull}

install -d %{buildroot}/%{_usrsrc}/%{githubfull}/c

install -d %{buildroot}/%{_usrsrc}/%{githubfull}/c/CAT_MBA
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CAT_MBA/Makefile          %{buildroot}/%{_usrsrc}/%{githubfull}/c/CAT_MBA
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CAT_MBA/README            %{buildroot}/%{_usrsrc}/%{githubfull}/c/CAT_MBA
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CAT_MBA/reset_app.c       %{buildroot}/%{_usrsrc}/%{githubfull}/c/CAT_MBA
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CAT_MBA/allocation_app_l2cat.c  %{buildroot}/%{_usrsrc}/%{githubfull}/c/CAT_MBA
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CAT_MBA/allocation_app_l3cat.c  %{buildroot}/%{_usrsrc}/%{githubfull}/c/CAT_MBA
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CAT_MBA/allocation_app_mba.c  %{buildroot}/%{_usrsrc}/%{githubfull}/c/CAT_MBA
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CAT_MBA/association_app.c %{buildroot}/%{_usrsrc}/%{githubfull}/c/CAT_MBA

install -d %{buildroot}/%{_usrsrc}/%{githubfull}/c/CMT_MBM
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CMT_MBM/Makefile      %{buildroot}/%{_usrsrc}/%{githubfull}/c/CMT_MBM
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CMT_MBM/README        %{buildroot}/%{_usrsrc}/%{githubfull}/c/CMT_MBM
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CMT_MBM/monitor_app.c %{buildroot}/%{_usrsrc}/%{githubfull}/c/CMT_MBM

install -d %{buildroot}/%{_usrsrc}/%{githubfull}/c/PSEUDO_LOCK
install -m 0644 %{_builddir}/%{githubfull}/examples/c/PSEUDO_LOCK/Makefile      %{buildroot}/%{_usrsrc}/%{githubfull}/c/PSEUDO_LOCK
install -m 0644 %{_builddir}/%{githubfull}/examples/c/PSEUDO_LOCK/README        %{buildroot}/%{_usrsrc}/%{githubfull}/c/PSEUDO_LOCK
install -m 0644 %{_builddir}/%{githubfull}/examples/c/PSEUDO_LOCK/dlock.c       %{buildroot}/%{_usrsrc}/%{githubfull}/c/PSEUDO_LOCK
install -m 0644 %{_builddir}/%{githubfull}/examples/c/PSEUDO_LOCK/dlock.h       %{buildroot}/%{_usrsrc}/%{githubfull}/c/PSEUDO_LOCK
install -m 0644 %{_builddir}/%{githubfull}/examples/c/PSEUDO_LOCK/pseudo_lock.c %{buildroot}/%{_usrsrc}/%{githubfull}/c/PSEUDO_LOCK
install -m 0644 %{_builddir}/%{githubfull}/examples/c/PSEUDO_LOCK/tsc.c         %{buildroot}/%{_usrsrc}/%{githubfull}/c/PSEUDO_LOCK
install -m 0644 %{_builddir}/%{githubfull}/examples/c/PSEUDO_LOCK/tsc.h         %{buildroot}/%{_usrsrc}/%{githubfull}/c/PSEUDO_LOCK

%files
%{_bindir}/pqos
%{_bindir}/pqos-os
%{_bindir}/pqos-msr
%{_mandir}/man8/pqos.8.gz
%{_mandir}/man8/pqos-os.8.gz
%{_mandir}/man8/pqos-msr.8.gz
%{_bindir}/rdtset
%{_mandir}/man8/rdtset.8.gz
%{_bindir}/membw
%{_mandir}/man8/membw.8.gz
%{_libdir}/libpqos.so.*

%{!?_licensedir:%global license %%doc}
%license %{_licensedir}/%{name}/LICENSE
%doc ChangeLog README.md

%files -n intel-cmt-cat-devel
%{_libdir}/libpqos.so
%{_libdir}/libpqos.so.5
%{_includedir}/pqos.h
%{_usrsrc}/%{githubfull}/c/CAT_MBA/Makefile
%{_usrsrc}/%{githubfull}/c/CAT_MBA/README
%{_usrsrc}/%{githubfull}/c/CAT_MBA/reset_app.c
%{_usrsrc}/%{githubfull}/c/CAT_MBA/association_app.c
%{_usrsrc}/%{githubfull}/c/CAT_MBA/allocation_app_l2cat.c
%{_usrsrc}/%{githubfull}/c/CAT_MBA/allocation_app_l3cat.c
%{_usrsrc}/%{githubfull}/c/CAT_MBA/allocation_app_mba.c
%{_usrsrc}/%{githubfull}/c/CMT_MBM/Makefile
%{_usrsrc}/%{githubfull}/c/CMT_MBM/README
%{_usrsrc}/%{githubfull}/c/CMT_MBM/monitor_app.c
%{_usrsrc}/%{githubfull}/c/PSEUDO_LOCK/Makefile
%{_usrsrc}/%{githubfull}/c/PSEUDO_LOCK/README
%{_usrsrc}/%{githubfull}/c/PSEUDO_LOCK/dlock.c
%{_usrsrc}/%{githubfull}/c/PSEUDO_LOCK/dlock.h
%{_usrsrc}/%{githubfull}/c/PSEUDO_LOCK/pseudo_lock.c
%{_usrsrc}/%{githubfull}/c/PSEUDO_LOCK/tsc.c
%{_usrsrc}/%{githubfull}/c/PSEUDO_LOCK/tsc.h
%doc %{_usrsrc}/%{githubfull}/LICENSE

%changelog
* Mon Feb 12 2024 Eugene Syromiatnikov <esyr@redhat.com> - 23.11-1
- Rebase to 23.11 (RHEL-25780)

* Mon Oct 12 2020 Jiri Olsa <jolsa@redhat.com> - 4.0.0-0
- New release 4.0.0

* Thu Jun 11 2020 Martin Cermak <mcermak@redhat.com> - 2.0.0-3
- NVR bump and rebuild because of CI gating.
  Related: #1682388

* Mon Oct 08 2018 Jiri Olsa <jolsa@redhat.com>  - 2.0.0-2
- New release 2.0.0-2
- passing distro CFLAGS/LDFLAGS

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
