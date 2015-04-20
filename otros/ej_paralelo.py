from mpi4py import MPI
import sys

size1 = MPI.COMM_WORLD.Get_size()
rank1 = MPI.COMM_WORLD.Get_rank()
name1 = MPI.Get_processor_name()

comm = MPI.COMM_WORLD  # comunicador entre dos procesadores

rank = comm.rank     # id procesador actual
size = comm.size     #
process = MPI.Get_processor_name()

if rank == 0:
    lista_enviar = [1, 2, 3]
    comm.send(lista_enviar, dest=1)
    comm.send(lista_enviar, dest=2)
    sys.stdout.write(
        "Hello, World! I am process %d of %d on %s.\n"
        % (rank1, size, process))
#    comm.send (lista_enviar, dest = 9)

if rank == 1:
    lista_recibir = comm.recv(source=0)
    lista_recibir.append(10)  # agregar al final #
    comm.send(lista_recibir, dest=0)
    sys.stdout.write(
        "Hello, World! I am process %d of %d on %s.\n"
        % (rank, size, process))

if rank == 2:
    lista_recibir = comm.recv(source=0)
    lista_recibir.append(7)  # agregar al final #
    comm.send(lista_recibir, dest=0)
    sys.stdout.write(
        "Hello, World! I am process %d of %d on %s.\n"
        % (rank, size, process))

if rank == 3:
    lista_recibir = comm.recv(source=0)
    lista_recibir.append(8)  # agregar al final #
    comm.send(lista_recibir, dest=0)
    sys.stdout.write(
        "Hello, World! I am process %d of %d on %s.\n"
        % (rank, size, process))

if rank == 0:
    lista_uno = comm.recv(source=1)
    lista_dos = comm.recv(source=2)
    sys.stdout.write(
        "Hello, World! I am process %d of %d on %s.\n"
        % (rank1, size1, name1))
    print "He recibido el ", lista_uno + lista_dos
