#include <sqlite3.h>
#include <string.h>

int main(void)
{
	return strcmp("3.14.1", sqlite3_version);
}
