#include <SwimServer.hpp>
#include <SwimClient.hpp>
#include <SwimCommon.hpp>

int main (void)
{
    swim::SwimServer server(9999);
    auto srv = swim::MakeServer("localhost", server.port());
    swim::SwimClient client(*srv);
    return 0;
}
