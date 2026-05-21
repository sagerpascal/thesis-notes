\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{jair-preprint}[2025/08/15 JAIR Preprint class extending acmart]

% Pass unknown options to acmart
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{acmart}}
\ProcessOptions\relax

% Load acmart with default options (acmlarge, screen)
\LoadClass[acmlarge,natbib=false,screen]{acmart}

% --- JAIR Customizations (Modified for arXiv preprint) ---
\RequirePackage{textcase}

% Remove ACM reference formatting by default
\settopmatter{printacmref=false}

% Removed doclicense package to prevent arXiv compilation issues
% \usepackage[...]{doclicense}

% Removed JAIR specific publication definitions
% \def\@journalName{Journal of Artificial Intelligence Research}%
% \def\@journalNameShort{JAIR}%
% \def\@permissionCodeOne{XXXX}%
% \def\@permissionCodeTwo{XXXX}%

%% JAIR Copyright Block - Emptied for preprint
\gdef\@copyrightpermission{}

% Removed DOI formatting for preprint
\def\@formatdoi#1{}

% Modified ORCID to prevent printing raw links in the addresses block
\renewcommand{\orcid}[2][]{%
  \unskip\ignorespaces
  \IfBeginWith{#2}{http}{%
    \if@ACM@anonymous\else
      % \g@addto@macro\addresses{\orcid{#2}{#2}}%
    \fi
  }{%
    \if@ACM@anonymous\else
      % \g@addto@macro\addresses{\orcid{https://orcid.org/#2}{#2}}%
    \fi
  }%
}

%% Jair AE and Track - Removed for plain version
% \def\JAIRAE#1{\def\@JAIRAE{#1}}
% \JAIRAE{Insert JAIR AE Name}
% \def\JAIRTrack#1{\def\@JAIRTrack{#1}}
% \JAIRTrack{Insert JAIR Track Name Here}

% JAIR specific section fonts (Kept from new template)
\def\@secfont{\sffamily\bfseries\large\section@raggedright}
\def\@subsecfont{\sffamily\bfseries\large\section@raggedright}

% --- Author Block Formatting (Kept intact from new JAIR template) ---
\def\@mkauthors@i{%
  \def\@currentauthors{}%
  \def\@currentaffiliations{}%
  \global\let\and\@typeset@author@line
  \def\@author##1{%
    \ifx\@currentauthors\@empty
      \gdef\@currentauthors{\@authorfont\MakeTextUppercase{##1}}%
    \else
       \g@addto@macro{\@currentauthors}{\and\MakeTextUppercase{##1}}%
    \fi
    \gdef\and{}}%
  \def\email##1##2{}%
  \def\orcid##1##2{}%
  \def\affiliation##1##2{%
    \def\@tempa{##2}\ifx\@tempa\@empty\else
       \ifx\@currentaffiliations\@empty
          \gdef\@currentaffiliations{%
            \setkeys{@ACM@affiliation@}{obeypunctuation=false}%
            \setkeys{@ACM@affiliation@}{##1}%
            \@ACM@resetaffil
            \@affiliationfont##2\@ACM@checkaffil}%
       \else
         \g@addto@macro{\@currentaffiliations}{\and
           \setkeys{@ACM@affiliation@}{obeypunctuation=false}%
           \setkeys{@ACM@affiliation@}{##1}\@ACM@resetaffil
           ##2\@ACM@checkaffil}%
      \fi
    \fi
     \global\let\and\@typeset@author@line}%
  \if@ACM@acmcp
    \advance\hsize by -6pc%
  \fi
  \global\setbox\mktitle@bx=\vbox{\noindent\unvbox\mktitle@bx\par\medskip
    \noindent\addresses\@typeset@author@line
   \par\medskip}%
}
\newbox\author@bx
\newdimen\author@bx@wd
\newskip\author@bx@sep
\author@bx@sep=1pc\relax
\def\@typeset@author@bx{\bgroup\hsize=\author@bx@wd
  \def\and{\par}\normalbaselines
  \global\setbox\author@bx=\vtop{\if@ACM@sigchiamode\else\centering\fi
    \@authorfont\@currentauthors\par\@affiliationfont
    \@currentaffiliation}\egroup
  \box\author@bx\hspace{\author@bx@sep}%
  \gdef\@currentauthors{}%
  \gdef\@currentaffiliation{}}
\def\@mkauthors@iii{%
  \author@bx@wd=\textwidth\relax
  \advance\author@bx@wd by -\author@bx@sep\relax
  \ifnum\@ACM@authorsperrow>0\relax
    \divide\author@bx@wd by \@ACM@authorsperrow\relax
  \else
    \ifcase\num@authorgroups
    \relax % 0?
    \or  % 1=one author per row
    \or  % 2=two authors per row
       \divide\author@bx@wd by \num@authorgroups\relax
    \or  % 3=three authors per row
       \divide\author@bx@wd by \num@authorgroups\relax
    \or  % 4=two authors per row (!)
       \divide\author@bx@wd by 2\relax
    \else % three authors per row
       \divide\author@bx@wd by 3\relax
    \fi
  \fi
  \advance\author@bx@wd by -\author@bx@sep\relax
  \gdef\@currentauthors{}%
  \gdef\@currentaffiliation{}%
  \def\@author##1{\ifx\@currentauthors\@empty
    \gdef\@currentauthors{\par##1}%
  \else
    \g@addto@macro\@currentauthors{\par##1}%
  \fi
  \gdef\and{}}%
  \def\email##1##2{\ifx\@currentaffiliation\@empty
    \gdef\@currentaffiliation{\bgroup
      \mathchardef\UrlBreakPenalty=10000\nolinkurl{##2}\egroup}%
  \else
    \g@addto@macro\@currentaffiliation{\par\bgroup
      \mathchardef\UrlBreakPenalty=10000\nolinkurl{##2}\egroup}%
  \fi}%
  \def\orcid##1##2{\ifx\@currentaffiliation\@empty
    \gdef\@currentaffiliation{\bgroup
      \mathchardef\UrlBreakPenalty=10000\nolinkurl{##2}\egroup}%
  \else
    \g@addto@macro\@currentaffiliation{\par\bgroup
      \mathchardef\UrlBreakPenalty=10000\nolinkurl{##2}\egroup}%
  \fi}%
  \def\affiliation##1##2{\ifx\@currentaffiliation\@empty
    \gdef\@currentaffiliation{%
      \setkeys{@ACM@affiliation@}{obeypunctuation=false}%
      \setkeys{@ACM@affiliation@}{##1}\@ACM@resetaffil
      ##2\@ACM@checkaffil}%
  \else
    \g@addto@macro\@currentaffiliation{\par
      \setkeys{@ACM@affiliation@}{obeypunctuation=false}%
      \setkeys{@ACM@affiliation@}{##1}\@ACM@resetaffil
      ##2\@ACM@checkaffil}%
  \fi
  \global\let\and\@typeset@author@bx
}%
  \hsize=\textwidth
  \global\setbox\mktitle@bx=\vbox{\noindent
    \unvbox\mktitle@bx\par\medskip\leavevmode
    \lineskip=1pc\relax\centering\hspace*{-1em}%
    \addresses\let\and\@typeset@author@bx\and\par\bigskip}}
\def\@mkauthors@iv{%
  \author@bx@wd=\columnwidth\relax
  \advance\author@bx@wd by -\author@bx@sep\relax
  \ifnum\@ACM@authorsperrow>0\relax
    \divide\author@bx@wd by \@ACM@authorsperrow\relax
  \else
    \ifcase\num@authorgroups
    \relax % 0?
    \or  % 1=one author per row
    \else  % 2=two authors per row
       \divide\author@bx@wd by 2\relax
    \fi
  \fi
  \advance\author@bx@wd by -\author@bx@sep\relax
  \gdef\@currentauthors{}%
  \gdef\@currentaffiliation{}%
  \def\@author##1{\ifx\@currentauthors\@empty
    \gdef\@currentauthors{\par##1}%
  \else
    \g@addto@macro\@currentauthors{\par##1}%
  \fi
  \gdef\and{}}%
  \def\email##1##2{\ifx\@currentaffiliation\@empty
    \gdef\@currentaffiliation{\nolinkurl{##2}}%
  \else
    \g@addto@macro\@currentaffiliation{\par\nolinkurl{##2}}%
  \fi}%
  \def\orcid##1##2{\ifx\@currentaffiliation\@empty
    \gdef\@currentaffiliation{\nolinkurl{##2}}%
  \else
    \g@addto@macro\@currentaffiliation{\par\nolinkurl{##2}}%
  \fi}%
  \def\affiliation##1##2{\ifx\@currentaffiliation\@empty
    \gdef\@currentaffiliation{%
      \setkeys{@ACM@affiliation@}{obeypunctuation=false}%
      \setkeys{@ACM@affiliation@}{##1}\@ACM@resetaffil
      ##2\@ACM@checkaffil}%
  \else
    \g@addto@macro\@currentaffiliation{\par
      \setkeys{@ACM@affiliation@}{obeypunctuation=false}%
      \setkeys{@ACM@affiliation@}{##1}\@ACM@resetaffil
      ##2\@ACM@checkaffil}%
  \fi
  \global\let\and\@typeset@author@bx}%
    \bgroup\hsize=\columnwidth
    \par\raggedright\leftskip=\z@
    \lineskip=1pc\noindent
    \addresses\let\and\@typeset@author@bx\and\par\bigskip\egroup}

% Emptied out Authors Addresses block at bottom of page 1
\def\@mkauthorsaddresses{}

% Cleaned up bib citation to remove JAIR specific metadata
\def\@mkbibcitation{\bgroup
  \let\@vspace\@vspace@orig
  \let\@vspacer\@vspacer@orig
  \def\@pages@word{\ifnum\getrefnumber{TotPages}=1\relax page\else pages\fi}%
  \def\footnotemark{}%
  \def\\{\unskip{} \ignorespaces}%
  \def\footnote{\ClassError{\@classname}{Please do not use footnotes
      inside a \string\title{} or \string\author{} command! Use
      \string\titlenote{} or \string\authornote{} instead!}}%
  \par\medskip\small\noindent{\bfseries Reference Format:}\par\nobreak
  \noindent\bgroup
    \def\\{\unskip{}, \ignorespaces}\authors\egroup. \@acmYear. \@title
  \ifx\@subtitle\@empty. \else: \@subtitle. \fi
  \par\egroup}  

% Removed JAIR headers/footers for a clean preprint
\AtBeginDocument{%
    \fancyfoot{}
  \fancypagestyle{firstpagestyle}{%
    \fancyhf{}%
  }%      
}

% Stripped maketitle to avoid printing permissions and author footnotes
\def\maketitle{\@beginmaketitlehook
  \@ACM@maketitle@typesettrue
  \if@ACM@anonymous
    \ifnum\num@authorgroups=0\author{}\fi
  \fi
  \begingroup
  \let\@vspace\@vspace@orig
  \let\@vspacer\@vspacer@orig
  \let\@footnotemark\@footnotemark@nolink
  \let\@footnotetext\@footnotetext@nolink
  \renewcommand\thefootnote{\@fnsymbol\c@footnote}%
  \hsize=\textwidth
  \def\@makefnmark{\hbox{\@textsuperscript{\@thefnmark}}}%
  \@mktitle\if@ACM@sigchiamode\else\@mkauthors\fi\@mkteasers
  \@printtopmatter
  \if@ACM@sigchiamode\@mkauthors\fi
  \setcounter{footnote}{0}%
  \def\@makefnmark{\hbox{\@textsuperscript{\normalfont\@thefnmark}}}%
  \@titlenotes
  \@subtitlenotes
  \@authornotes
  \let\@makefnmark\relax
  \let\@thefnmark\relax
  \let\@makefntext\noindent
  \ifx\@empty\thankses\else
    \footnotetextauthorsaddresses{%
      \def\par{\let\par\@par}\parindent\z@\@setthanks}%
  \fi
  \endgroup
  \if@ACM@engage\@typesetengagemetadata\fi
  \setcounter{footnote}{0}%
  \@mkabstract
  \ifx\@translatedabstracts\@empty\else
  \@translatedabstracts\fi
  \if@ACM@printccs
  \ifx\@concepts\@empty\else\bgroup
      {\@specialsection{CCS Concepts}%
         \noindent\@concepts\par}\egroup
      \fi
    \fi
    \if@ACM@acmcp\else
      \ifx\@keywords\@empty\else\bgroup
        {\@specialsection{\keywordsname}%
           \noindent\@keywords\par}\egroup
      \fi
    \ifx\@translatedkeywords\@empty\else
       \@translatedkeywords
    \fi
  \fi
  \let\metadata@authors=\authors
  \nxandlist{, }{, }{, }\metadata@authors
  \def\@ACM@checkaffil{}%
  \hypersetup{%
    pdfauthor={\metadata@authors},
    pdftitle={\@title},
    pdfsubject={\@concepts},
    pdfkeywords={\@keywords},
    pdfcreator={LaTeX with acmart
      \csname ver@\@classname.cls\endcsname\space
      and hyperref
      \csname ver@hyperref.sty\endcsname}}%
  \andify\authors
  \andify\shortauthors
  \global\let\authors=\authors
  \global\let\shortauthors=\shortauthors
  \if@ACM@printacmref
     \@mkbibcitation
  \fi
  \global\@topnum\z@ 
  \global\@botnum\z@ 
  \@printendtopmatter
  \@afterindentfalse
  \@afterheading
  \if@ACM@acmcp
    \set@ACM@acmcpbox
    \AtEndDocument{\end@ACM@color@frame}%
    \@ACM@color@frame
  \fi
}