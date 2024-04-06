#include <SwimServer.hpp>
#include <SwimClient.hpp>
#include <SwimCommon.hpp>

int main (void)
{
    swim::SwimServer server("localhost",9999);
    auto srv = swim::MakeServer("localhost", server.port());
    swim::SwimClient client("localhost", 0, *srv);
    return 0;
}
