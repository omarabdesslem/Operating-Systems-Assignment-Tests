void die(char* motive);
uint8_t get_rdm_nbr();
int CSwrite(int fd, uint16_t *buf);
int CSread(int fd, uint16_t *buf);
void handleClient( int cfd, pid_t pid);
void client_request(int cfd);