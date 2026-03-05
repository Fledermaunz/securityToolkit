// bpaf parsing command line arguments
use bpaf::Bpaf;
// io & net for input/output and network operations
use std::io::{self, Write};
use std::net::{IpAddr, Ipv4Addr};
// sync for message passing between threads
use std::sync::mpsc::{channel, Sender};
//tokio asynchronous programming
use tokio::net::TcpStream;  
use tokio::task;

const MAX: u16 = 65535; //max value for end port
// default ip address (localhost)
const IPFALLBACK: IpAddr = IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1));

pub struct Args {
    //input
    #[bpaf(long, short, argument("Address"), fallback(IPFALLBACK))]
    pub address: IpAddr,
    #[bpaf(long("start"), short('s'), guard(start_port_guard, "Must be greater than 0"), fallback(1u16))]
    pub start_port: u16,
    #[bpaf(long("end"), short('e'), guard(end_port_guard, "Must be less or equal to 65535"), fallback(MAX))]
    end_port: u16,
}

async fn scan(tx: Sender<u16>, start_port: u16, addr: IpAddr){
    //portscan
    match TcpStream::connect(format!("{}:{}", addr, start_port)).await{
        Ok(_) => {
            print!(".");
            io::stdout().flush().unwrap();
            tx.send(start_port).unwrap();
        }
        Err(_) => {}
    }
}

fn start_port_guard(port: &u16) -> bool {
    *port > 0
}

fn end_port_guard(port: &u16) -> bool {
    *port <= MAX
}

#[tokio::main]
async fn main(){
    println!("Port Scanner");
}


