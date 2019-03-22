
import dgilib_threaded as dgi_t


data, processed_data = dgi_t.start()
dgi_t.wait_dgilib()
dgi_t.wait_sendrecv()