#include <iostream>
#include <sqlite3.h>

int main(void)
{
    std::cout << "SQLite3 " << sqlite3_libversion() << std::endl;
    return 0;
}

