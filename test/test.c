#include <sqlite3.h>
#include <string.h>

int main(void)
{
	return strcmp("3.10.2", sqlite3_version);
}
