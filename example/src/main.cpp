#include <iostream>

#include <version/Build.h>

int main()
{
	std::cout << "Hello, World!" << std::endl;
	std::cout << std::endl;
	std::cout << "getVersion: " << Build::getVersion() << std::endl;
	std::cout << "getDate: " << Build::getDate() << std::endl;
	std::cout << std::endl;
	std::cout << "Git::getSHA1Short: " << Build::Git::getSHA1Short() << std::endl;
	std::cout << "Git::getSHA1Full: " << Build::Git::getSHA1Full() << std::endl;
	std::cout << "Git::getCommitDate: " << Build::Git::getCommitDate() << std::endl;
	std::cout << "Git::isDirty: " << Build::Git::isDirty() << std::endl;
	return 0;
}
