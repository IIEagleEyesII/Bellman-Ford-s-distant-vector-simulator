import NetworkSimulator

if __name__ == '__main__':
    event_queue = []
    current_time = 0
    simulator = NetworkSimulator.NetworkSimulator('simulation.json')
    simulator.spark()
    print("*"*100)
    print('\n routers dvtables :\n')
    routers = simulator.get_routers()
    for router in routers:
        print(router.get_dv_table())


    simulator2 = NetworkSimulator.NetworkSimulator('simulation.json')
    simulator2.run()
    print("*" * 100)
    print('\n routers dvtables 2:\n')
    routers2 = simulator2.get_routers()
    for router in routers2:
        print(router.get_dv_table())


