%global pkg_name avalon-logkit
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global     short_name      logkit
%global     camelcase_short_name      LogKit

Name:        %{?scl_prefix}%{pkg_name}
Version:     2.1
Release:     14.11%{?dist}
Epoch:       0
Summary:     Java logging toolkit
License:     ASL 2.0
URL:         http://avalon.apache.org/%{short_name}/
Source0:     http://archive.apache.org/dist/excalibur/%{pkg_name}/source/%{pkg_name}-%{version}-src.zip
Source1:     http://repo1.maven.org/maven2/avalon-logkit/avalon-logkit/%{version}/%{pkg_name}-%{version}.pom
Patch0:      fix-java6-compile.patch
Patch1:      avalon-logkit-pom-deps.patch
Patch2:      avalon-logkit-encoding.patch
Patch3:      java7.patch

BuildRequires:    %{?scl_prefix_java_common}javapackages-tools
BuildRequires:    %{?scl_prefix_java_common}ant
BuildRequires:    %{?scl_prefix_java_common}javamail
BuildRequires:    %{?scl_prefix_java_common}ant-junit
BuildRequires:    %{?scl_prefix_java_common}log4j
BuildRequires:    %{?scl_prefix_java_common}tomcat-servlet-3.0-api
BuildRequires:    %{?scl_prefix}avalon-framework >= 0:4.1.4
# Required for converting jars to OSGi bundles
BuildRequires:    %{?scl_prefix}aqute-bnd
BuildRequires:    %{?scl_prefix}geronimo-jms

Requires:    %{?scl_prefix}avalon-framework >= 0:4.1.4
Requires:    %{?scl_prefix}geronimo-jms
Requires:    %{?scl_prefix_java_common}tomcat-servlet-3.0-api
Requires:    %{?scl_prefix_java_common}javamail

BuildArch:    noarch


%description
LogKit is a logging toolkit designed for secure performance orientated
logging in applications. To get started using LogKit, it is recomended
that you read the whitepaper and browse the API docs.

%package javadoc
Summary:    Javadoc for %{pkg_name}

%description javadoc
Javadoc for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%patch0

cp %{SOURCE1} pom.xml
%patch1
%patch2 -p1
%patch3
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
export CLASSPATH=$(build-classpath log4j javamail/mailapi jms tomcat-servlet-api jdbc-stdext avalon-framework junit):$PWD/build/classes
ant -Dencoding=ISO-8859-1 -Dnoget=true clean jar javadoc
# Convert to OSGi bundle
java -jar $(build-classpath aqute-bnd) wrap target/%{pkg_name}-%{version}.jar
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -d -m 755 $RPM_BUILD_ROOT/%{_mavenpomdir}

install -m 644 target/%{pkg_name}-%{version}.bar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}.jar

install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{pkg_name}.pom
%add_maven_depmap JPP-%{pkg_name}.pom %{pkg_name}.jar -a "%{short_name}:%{short_name},org.apache.avalon.logkit:%{pkg_name}"

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt

%files javadoc
%doc LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}

%changelog
* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 0:2.1-14.11
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michael Simacek <msimacek@redhat.com> - 0:2.1-14.10
- BR/R on packages from rh-java-common

* Wed Jan 07 2015 Michal Srb <msrb@redhat.com> - 2.1-14.9
- Migrate to .mfiles

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 0:2.1-14.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.1-14.7
- Mass rebuild 2014-05-26

* Fri Mar 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.1-14.6
- Add missing requires on javamail

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.1-14.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.1-14.4
- Mass rebuild 2014-02-18

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.1-14.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.1-14.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.1-14.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 02.1-14
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.1-13
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 21 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.1-11
- Change build-classpath call from macro to shell expansion

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.1-10
- Fix license tag
- Install NOTICE file

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Alexander Kurtakov <akurtako@redhat.com> 0:2.1-8
- Another Java 7 fix.
- BR/R servlet 3.0 api.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.1-6
- aqute-bndlib renamed to aqute-bnd (#745166)
- Fix compilation with openjdk 1.7.0
- Use new maven macros
- Packaging tweaks

* Fri May  6 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.1-5
- Fix up depdenencies in pom

* Tue May 3 2011 Severin Gehwolf <sgehwolf@redhat.com> 0:2.1-4
- Convert jar's to OSGi bundles using aqute-bndlib.

* Thu Apr 21 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.1-3
- Add maven metadata into package
- Tweaks according to new guidelines

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 9 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.1-2
- Add missing ant-junit BR.

* Tue Nov 9 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.1-1
- Update to 2.1 (rhbz#599622).

* Tue Nov  9 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2-9
- Fix build to use tomcat6
- Cleanups, various packaging problems fixed

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.2-6
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.2-5jpp.5
- Autorebuild for GCC 4.3

* Fri Feb 09 2007 Permaine Cheung <pcheung@redhat.com> 0:1.2-4jpp.5%{?dist}
- Fix source URL, BuildRoot

* Thu Feb 08 2007 Permaine Cheung <pcheung@redhat.com> 0:1.2-4jpp.4%{?dist}
- rpmlint cleanup.

* Thu Aug 03 2006 Deepak Bhole <dbhole@redhat.com> 0:1.2-4jpp.3
- Added missing requirements.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.2-4jpp_2fc
- Rebuilt

* Wed Jul 19 2006 Deepak Bhole <dbhole@redhat.com> 0:1.2-4jpp_1fc
- Added conditional native compilation.
- Removed name/release/version defines as applicable.

* Fri Aug 20 2004 Ralph Apel <r.apel@r-apel.de> 0:1.2-3jpp
- Build with ant-1.6.2

* Fri May 09 2003 David Walluck <david@anti-microsoft.org> 0:1.2-2jpp
- update for JPackage 1.5

* Fri Mar 21 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 1.2-1jpp
- For jpackage-utils 1.5

* Tue May 07 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0.1-4jpp
- hardcoded distribution and vendor tag
- group tag again

* Thu May 2 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0.1-3jpp
- distribution tag
- group tag

* Mon Mar 18 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0.1-2jpp
- generic servlet support

* Sun Feb 03 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0.1-1jpp
- 1.0.1
- versioned dir for javadoc
- no dependencies for and javadoc package
- adaptation for new servlet3 package
- drop j2ee package
- regenerated the patch
- section package

* Wed Dec 5 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-4jpp
- javadoc into javadoc package
- Requires and BuildRequires servletapi3 >= 3.2.3-2
- regenerated the patch

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.0-3jpp
- changed extension --> jpp

* Tue Nov 20 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-2jpp
- non-free extension classes back in original archive
- removed packager tag

* Sun Oct 28 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-1jpp
- 1.0

* Tue Oct 9 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-0.b5.2jpp
- non-free extension as additional package

* Sat Oct 6 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-0.b5.1jpp
- 1.0b5
- first unified release
- used original tarball

* Mon Sep 10 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-0.b4.1mdk
- first Mandrake release
