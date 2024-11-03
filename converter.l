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
    int schim;

    #define STEP_SCHEMANTIC do { \
			schim = 0; \
			int re = fread(schemantic, sizeof(char), MAX_SHIMS, build_file); \
			if (re != sizeof(char)*MAX_SHIMS) { printf("- %d\n", re); exit(2); } \
		} while (0)
    #define ECHOS(s) fwrite(s, strlen(s), 1, yyout)
%}

comment_marker  (\/\*)|(\*\/)
identifier      \$?[A-Za-z0-9_]+
modify          [+-]{2}
assignment      ([+-/*%!]|(<<)|(>>))=
shift           (<<)|(>>)

word    {identifier}
special {comment_marker}|{assignment}|{shift}|{modify}

%x IN_STRING

    // Keep all but the required whitespaces
%x NORMALIZE
    // Count the non-required whitespaces and write python arrays
%x ACCUMULATE
    // Reconstruct normalized file based on binary whitespace count arrays
%x BUILD

%option yylineno
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
\n          { ECHO; }
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
[ ]         { ECHO; }
{word}|{special}|.    {
                for (char i = 0; i < schemantic[schim]; i++) {
                    ECHOS(" ");
                }
                ECHO;

                ++schim;
            }
\n          { // XXX we find the last newline and still step, resulting in an error
				ECHO;
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
        puts(
			"Usage:\n"
			"$ converter normalize  [<file>|^<string>]\n"
			"$ converter accumulate [<file>|^<string>]\n"
			"$ converter build      [<file>|^<string>] <schemantic-file>\n"
		);
        return 1;
    }

    if (!strcmp(argv[1], "normalize")) {
        mystate = NORMALIZE;
    } else
    if (!strcmp(argv[1], "accumulate")) {
        mystate = ACCUMULATE;
    } else
    if (!strcmp(argv[1], "build")) {
		if (argc < 4) { exit(4); }
        mystate = BUILD;
        build_file = fopen(argv[3], "rb");
		if (!build_file) { exit(1); }
        STEP_SCHEMANTIC;
    } else {
        return 1;
    }

	char * input;
	if (argv[2][0] == '^') {
		input = (char*)argv[2]+1;
	} else {
		FILE * f = fopen(argv[2], "r");
		if(!f){ exit(3); }
		fseek(f, 0, SEEK_END);
		int flen = ftell(f);
		rewind(f);
		input = malloc(flen+1);
		input[flen] = '\00';
		fread(input, flen, sizeof(char), f);
		fclose(f);
	}

	YY_BUFFER_STATE const b = yy_scan_string(input);
    yylex();
	yy_delete_buffer(b);

    return 0;
}
