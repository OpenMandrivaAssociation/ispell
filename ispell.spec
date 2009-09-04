#
# NOTE:
#
# ispell dictionaries are no longer used on mandrakelinux;
# being replaced with aspell.
# ispell is only being kept for people that may have personal
# spell checking dictionnaries using affix compression; as
# currently aspell doesn't support it; once aspell (version 6) will
# be out, ispell will be removed.
#
# the package ispell-en has been removed, as well as the dependnece
# of "ispell-dictionnary" from ispell.
# if you want to revert that, search for "aspell" in this spec file

Summary:	The GNU interactive spelling checker program
Name:		ispell
Version:	3.2.06
Release:	%mkrel 15
Group:		Text tools

URL:		http://ficus-www.cs.ucla.edu/ficus-members/geoff/ispell.html

Source0:	http://fmg-www.cs.ucla.edu/geoff/tars/ispell-%{version}.tar.bz2
Source2:	spell.bz2
Source3:	ispell-3.20-hk2-deutsch.tar.bz2 

Patch0:		ispell-3.1.20-config.patch.bz2
Patch1:		ispell-3.2.06-german.patch.bz2 
Patch3:		ispell-3.1.20-termio.patch.bz2
Patch5:		ispell-3.1.20-strcmp.patch.bz2
Patch6:		ispell-3.1.20-maskbits64_and_british.patch.bz2 
# maybe obsolete
#Patch7:	ispell-3.1.20-fixinfo.patch.bz2
Patch8:		ispell-3.2.06-dont-string.patch.bz2
# maybe obsolete
#Patch10:	ispell-fix-info-file.patch.bz2
# maybe obsolete
Patch11:	ispell-3.20-man-update.patch.bz2
Patch12:	ispell-3.20-sh.patch.bz2
# obsolete
#Patch13:	ispell-3.20-sq-fixes.patch.bz2
# obsolete
#Patch14:	ispell-3.20-sq-fixes2.patch.bz2
Patch15:	ispell-3.20-missing_prototypes.patch.bz2
Patch17:	ispell-3.20-increase-max.patch.bz2
#Patch18:	ispell-3.20-iso-more-html.patch.bz2
Patch19:	ispell-3.20-xb-options.patch.bz2
# patch to add recognition of non-alphanumeric chars between ascii A-z as
# flags; needed by latest norwegian ispell *.aff files -- pablo
Patch20:	ispell-3.2.06.no.patch.bz2
# patch to add sq and unsq programs missing from 3.2.06, but needed
# by some ispell packages -- pablo
Patch21:	ispell-3.2.06-sq.patch.bz2
# add missing includes
Patch22:	ispell-3.2.06-includes.patch.bz2
# use mkdir -p to create directories
Patch23:	ispell-3.2.06-mkdir_p.patch.bz2

License:	GPL
BuildRequires:	byacc ncurses-devel
BuildRoot:	%_tmppath/%name-%version-%release-buildroot
# we don't distribute ispell dictionnaries anymore, as they are
# replaced with aspell ones
#Requires:	ispell-dictionary == 3.2.06

%description
Ispell is the GNU interactive spelling checker.  Ispell will check a text
file for spelling and typographical errors.  When it finds a word that is
not in the dictionary, it will suggest correctly spelled words for the
misspelled word.

You should install ispell if you need a program for spell checking (and who
doesn't...).

Note this package has only the spell checker engine; you also need to
install the dictionary files from the ispell-* package for your language.

%package en
Summary:	English dictionary for ispell
Group:		System/Internationalization
# the binary format changed with ispell 3.2.06
Requires:	ispell >= 3.2.06-2mdk
Requires:	locales-en
BuildRequires:	words >= 2-16mdk
Obsoletes:	iamerica ispell-english ibritish ispell-british ispell-dictionary
Provides:	iamerica ispell-english ibritish ispell-british
Provides:	ispell-dictionary = 3.2.06

%description en
This package has the English dictionary files for ispell.

With it you can check the spelling of English text files or LaTeX files
written in English.

%prep

%setup -q -n ispell-%{version} -a3

%patch0 -p1
%patch1 
%patch3 -p1 -b .termio


%patch5 -p1 -b .strcmp
%patch6 -p1 -b .maskbits

# info pages missing from 3.2.06 sources -- pablo
#
#%patch7 -p1 -b .makeinfo
%patch8 -p1
# info pages missing from 3.2.06 sources -- pablo
#
#%patch10 -p0
%patch12 -p1
%patch15 -p1
%patch17 -p1
#%patch18 -p0 -b .html
%patch19 -p1
%patch20 -p1 -b .NO
%patch21 -p1 -b .SQ
%patch11 -p1
%patch22 -p1 -b .includes
%patch23 -p1 -b .mkdir-p

%build
export LC_ALL='en'
# Make config.sh first
TMPDIR=%_tmppath PATH=.:$PATH make CFLAGS="$RPM_OPT_FLAGS" config.sh
perl -p -i -e "s/-O/$RPM_OPT_FLAGS/" config.sh

# (Dadou) - 3.1.20-12mdk OK, it's ugly but it's late and I have no time to do
# nice things. Do them  if you want. Maintener (Pablo) s***s (sorry)
perl -pi -e "s#/usr/man#/usr/share/man#g" config.sh
perl -pi -e "s#/usr/info#/usr/share/info#g" config.sh
perl -pi -e "s#MASTERHASH='americanmed.hash'#MASTERHASH='americanmed+.hash'#g" config.sh
perl -pi -e "s#/usr/dict/words#/usr/share/dict/words#g" local.h
perl -pi -e "s#/usr/dict/words#/usr/share/dict/words#g" config.X
perl -pi -e "s#/usr/dict/words#/usr/share/dict/words#g" config.sh
perl -pi -e "s#/usr/dict/words#/usr/share/dict/words#g" ispell.1X
perl -pi -e "s#/usr/dict/words#/usr/share/dict/words#g" ispell.el
perl -pi -e "s#/usr/dict/words#/usr/share/dict/words#g" sq.1

# Now save build-rooted version (with time-stamp) for install ...
cp config.sh config.sh.BUILD
sed -e "s,/usr/,$RPM_BUILD_ROOT/usr/,g" < config.sh.BUILD > config.sh.INSTALL

# and then make everything
TMPDIR=%_tmppath PATH=.:$PATH make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%_mandir
mkdir -p $RPM_BUILD_ROOT%_libdir/emacs/site-lisp
mkdir -p $RPM_BUILD_ROOT%_infodir

# Roll in the build-root'ed version (with time-stamp!)
cp -f config.sh.INSTALL config.sh
TMPDIR=%_tmppath PATH=.:$PATH make install

# fix LIBDIR in munchlist
perl -pi -e "s#^LIBDIR=.*#LIBDIR=/usr/lib/ispell#" $RPM_BUILD_ROOT%{_bindir}/munchlist

# info pages missing from 3.2.06 sources -- pablo
#
#mv $RPM_BUILD_ROOT%_infodir/ispell $RPM_BUILD_ROOT%_infodir/ispell.info

bzcat %{SOURCE2} >$RPM_BUILD_ROOT%{_bindir}/spell

# Remove unpackaged files which turn out to be (or should be) in ispell-de
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/ispell/{deutsch*.{aff,hash},german*}

# we don't build ispell-en anymore (replaced with aspell-en)
# so we remove its files
rm -f $RPM_BUILD_ROOT%{_mandir}/man4/english.4*
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/ispell/*.hash
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/ispell/*.aff

%clean
rm -fr $RPM_BUILD_ROOT

# info pages missing from 3.2.06 sources -- pablo
#
#%post
#%_install_info %name.info
#
#%postun
#%_remove_install_info %name.info

%files
%defattr(-,root,root)
%doc README
%attr(755,root,root) %_bindir/*
%_mandir/man1/ispell.1*
%_mandir/man4/ispell.4*
# info pages missing from 3.2.06 sources -- pablo
#%_infodir/ispell.info*
#%_libdir/emacs/site-lisp/ispell.el
%_mandir/man1/buildhash.1*
%_mandir/man1/munchlist.1*
%_mandir/man1/findaffix.1*
%_mandir/man1/tryaffix.1*
%_mandir/man1/sq.1*
%_mandir/man1/unsq.1*
%dir %_prefix/lib/ispell

# We don't build ispell-en anymore; replaced with aspell-en
#%files en
#%defattr(-,root,root)
#%_mandir/man4/english.4*
#%_prefix/lib/ispell/american.hash
#%_prefix/lib/ispell/americanmed+.hash
#%_prefix/lib/ispell/americanxlg.hash
#%_prefix/lib/ispell/english.aff
#%_prefix/lib/ispell/english.hash
#%_prefix/lib/ispell/british.hash
#%_prefix/lib/ispell/britishmed+.hash
#%_prefix/lib/ispell/britishxlg.hash

