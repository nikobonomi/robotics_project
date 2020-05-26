from client.WallLover import WallLover

if __name__ == '__main__':
    # creo un instanza del robot
    controller = WallLover()

    # lo simulo finche posso
    while True:
        controller.step()
        controller.rate_keeper.wait_cycle()