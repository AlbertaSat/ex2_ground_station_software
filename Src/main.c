#include <FreeRTOS.h>
#include <csp/csp.h>
#include "system.h"

SAT_returnState init_local_gs(void);

#ifdef USE_LOCAL_GS
csp_iface_t csp_if_fifo = {
    .name = "fifo",
    .nexthop = csp_fifo_tx,
    .mtu = TM_TC_BUFF_SIZE,
};
#endif

int main(int argc, char **argv) {
  TC_TM_app_id my_address = GND_APP_ID;

  #ifdef USE_LOCAL_GS
  init_local_gs();
  csp_iface_t this_interface = csp_if_fifo;
  #else
  // implement other interfaces
  #endif

  /* Init CSP and CSP buffer system */
  if (csp_init(my_address) != CSP_ERR_NONE ||
      csp_buffer_init(64, 512) != CSP_ERR_NONE) {
    printf("Failed to init CSP\r\n");
    return -1;
  }

  /* Set default route and start router & server */
  csp_route_set(CSP_DEFAULT_ROUTE, &this_interface, CSP_NODE_MAC);
  csp_route_start_task(0, 0);

  xTaskCreate((TaskFunction_t)server_loop, "SERVER THREAD", 2048, NULL, 1,
              NULL);

  vTaskStartScheduler();

  for (;;) {
  }

  close(rx_channel);
  close(tx_channel);

  return 0;
}

SAT_returnState init_local_gs(void) {
  char *tx_channel_name = "client_to_server";
  char *rx_channel_name = "server_to_client";

  tx_channel = open(tx_channel_name, O_RDWR);
  if (tx_channel < 0) {
    printf("Failed to open TX channel\r\n");
    return -1;
  }

  rx_channel = open(rx_channel_name, O_RDWR);
  if (rx_channel < 0) {
    printf("Failed to open RX channel\r\n");
    return -1;
  }

  /* Start fifo RX task */
  xTaskCreate((TaskFunction_t)fifo_rx, "RX_THREAD", 2048, NULL, 1, NULL);
}
