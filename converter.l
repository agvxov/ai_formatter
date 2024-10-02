/* @BAKE
    flex -o $*.yy.c $@
    gcc -o $*.out $*.yy.c
   @STOP
 */
%{
    /* NOTE: this shall be compiled as a shared library so python may call in
    */
    /* XXX: we have a problem on nuking system includes;
             this fucks with trying to be language agnostic;
             i wonder if hopefully the AI can just realize theres never spaces there
    */
    #include <stdio.h>

    int mystate;

    int accumulator = 0;

    #define ECHOS(s) fwrite(s, strlen(s), 1, yyout)

    #define EOL '\n'
%}

comment_marker  (\/\*)|(\*\/)
identifier      \$?[A-Za-z0-9_]+
modify          [+-]{2}
assignment      ([+-/*%]|(<<)|(>>))=
shift           (<<)|(>>)

word    {identifier}|{comment_marker}|{assignment}|{shift}|{modify}

%x NORMALIZE ACCUMULATE
%x IN_STRING
%option noyywrap nodefault
%%
    BEGIN mystate;
    if (mystate == ACCUMULATE) {
        ECHOS("[");
    }

<NORMALIZE>{
[ ]|\t      { ; }
\"          {
                ECHO;
                BEGIN IN_STRING;
            }
{word}|.    {
                ECHO;
                ECHOS(" ");
            }
\n          {
                ECHO;
                return EOL;
            }
}

<ACCUMULATE>{
[ ]         {
                ++accumulator;
            }
\t          {
                accumulator += 4;
            }
\"          {
                BEGIN IN_STRING;
            }
{word}|.    {
                printf("%d, ", accumulator);
                accumulator = 0;
            }
\n\n        {
                ECHOS("]\n[0]\n[");
            }
\n          {
                ECHOS("]\n[");
            }
}

<IN_STRING>{
\\\"    {
            if (mystate == NORMALIZE) {
                ECHO;
            }
        }
\"      {
            if (mystate == NORMALIZE) {
                ECHO;
            }
            BEGIN mystate;
        }
.|\n    {
            if (mystate == NORMALIZE) {
                ECHO;
            }
        }
}
%%

signed main(const int argc, const char * const * const argv) {
    if (argc < 3) {
        puts("Usage: converter <mode> <file>");
        return 1;
    }

    if (!strcmp(argv[1], "normalize")) {
        mystate = NORMALIZE;
    } else
    if (!strcmp(argv[1], "accumulate")) {
        mystate = ACCUMULATE;
    } else {
        return 1;
    }

    yyin = fopen(argv[2], "r");

    while(yylex() == EOL) { ; }

    return 0;
}
