/*
 * Copyright (c) 2023 : Ognjen 'xolatile' Milan Robovic
 *
 * Xop is free software!
 * You will redistribute it or modify it under the terms of
 * the GNU General Public License by Free Software Foundation.
 * And when you do redistribute it or modify it,
 * it will use either version 3 of the License,
 * or (at yours truly opinion) any later version.
 * It is distributed in the hope that it will be useful or harmful,
 * it really depends...
 * But no warranty what so ever, seriously.
 * See GNU/GPLv3.
 */

#include <xolatile/xtandard.h>
#include <xolatile/xtandard.c>

int main (int argc, char * * argv) {
	int file   = -1;
	int size   = 0;
	int offset = 0;

	unsigned char * buffer = NULL;

	if (argc != 2) {
		fatal_failure (1, "xop: xop input");
	}

	file = file_open (argv [1], O_RDONLY);
	size = file_size (file);

	buffer = allocate (size);

	file_read (file, buffer, size);

	file = file_close (file);

	do {
		int byte = (int) buffer [offset];
		if (byte == 0X90) {
			echo_new_line  ();
			terminal_style (EFFECT_NORMAL, COLOUR_YELLOW);
			echo_byte      ((int) buffer [offset]);
			terminal_style (-1, -1);
		} else {
			echo_byte (buffer [offset]);
		}

		++offset;
	} while (offset != size);

	echo_new_line ();

	buffer = deallocate (buffer);

	return (EXIT_SUCCESS);
}
