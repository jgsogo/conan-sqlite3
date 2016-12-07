#include <iostream>
#include <sqlite3.h>
#include <string.h>

int main(void)
{
    std::cout << "SQLite3 test" << std::endl;
    return strcmp("3.14.1", sqlite3_version);
}

