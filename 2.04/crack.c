#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int verify(unsigned int v0, unsigned int v1, unsigned int v2, unsigned int v3)
{
	if (!v0 || !v1 || !v2 || !v3)
		return 0;
	if (v1 * v0 + v2 - v3 != 1208779703)
		return 0;
	if (v1 - v0 != -24223)
		return 0;
	if (v3 - 5 * v2 == -129519)
		return (v3 + v1) % 100000 == 40256;
	return 0;
}

int main()
{
	for (unsigned int v1 = 1; v1 < 75777; v1++)
	{
		unsigned int v0 = v1 + 24223;
		for (unsigned int v2 = 25904; v2 < 45904; v2++)
		{
			unsigned int v3 = (5 * v2) - 129519;
			if (verify(v0, v1, v2, v3))
			{
				printf("%u-%u-%u-%u\n", v0, v1, v2, v3);
				return 0;
			}
		}
	}
	return 0;
}