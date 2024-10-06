/* @BAKE
    flex -o $*.yy.c $@
    gcc -o $*.out $*.yy.c
   @STOP
 */
%{
    #include <stdio.h>
    #include <stdbool.h>

    #define LINE_WIDTH 80
    #define MAX_SHIMS  LINE_WIDTH - 1

    int mystate;

    bool was_word = false;

    int accumulator = 0;

    FILE * build_file;
    char schemantic[MAX_SHIMS];
    int schim = 0;

    #define STEP_SCHEMANTIC fread(schemantic, MAX_SHIMS, sizeof(char), build_file)
    #define ECHOS(s) fwrite(s, strlen(s), 1, yyout)

    #define EOL '\n'
%}

comment_marker  (\/\*)|(\*\/)
identifier      \$?[A-Za-z0-9_]+
modify          [+-]{2}
assignment      ([+-/*%]|(<<)|(>>))=
shift           (<<)|(>>)

word    {identifier}
special {comment_marker}|{assignment}|{shift}|{modify}

%x NORMALIZE ACCUMULATE BUILD
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
{word}      {
                if (was_word) {
                    ECHOS(" ");
                }
                ECHO;
                was_word = true;
            }
{special}|. {
                ECHO;
                was_word = false;
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
{word}      {
                if (was_word) {
                    --accumulator;
                }
                was_word = true;
                printf("%d, ", accumulator);
                accumulator = 0;
            }
{special}|. {
                was_word = false;
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

<BUILD>{
[ ]|\t      { ; }
{word}|.    {
                ECHO;
                for (char i = 0; i < schemantic[schim]; i++) {
                    ECHOS(" ");
                }
                ++schim;
            }
\n          {
                STEP_SCHEMANTIC;
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
    } else
    if (!strcmp(argv[1], "build")) {
        mystate = BUILD;
        build_file = fopen("build_file", "rb");
        STEP_SCHEMANTIC;
    } else {
        return 1;
    }

    yyin = fopen(argv[2], "r");

    while(yylex() == EOL) { ; }

    return 0;
}
