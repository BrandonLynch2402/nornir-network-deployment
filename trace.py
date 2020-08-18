from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command, netmiko_send_config, napalm_get
from nornir.plugins.functions.text import print_result
from rich import pretty, print

pretty.install()

def get_facts(task):
    r = task.run(
        napalm_get,
        getters=['lldp_neighbors', 'facts']
    )

    task.host['facts'] = r.result

def main() -> None:
    nr = InitNornir(config_file='config.yaml')
    result = nr.run(task=get_facts)
    print_result(result)
    import ipdb;
    ipdb.set_trace()

if __name__ == '__main__':
    main()
