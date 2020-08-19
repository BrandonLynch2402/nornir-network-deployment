from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command, netmiko_send_config, napalm_get
from nornir.plugins.functions.text import print_result

def deployment(task):
    
    # Gather LLDP information and facts
    r = task.run(
        napalm_get,
        getters=['lldp_neighbors', 'facts']
    )
    task.host['store'] = r.result


    # Remove VLANs
    task.run(netmiko_send_config, config_commands=['no vlan 2-101'])


    # Remove trunk ports
    trunk_port_list = task.host['store']['lldp_neighbors'].keys()
    trunk_commands = []    
    for trunk_port in trunk_port_list:
        trunk_commands.extend((
            f"interface {trunk_port}",
            "no description",
            "switchport mode access",
            "no switchport trunk encapsulation dot1q",
            "no switchport nonegotiate",
            "no switchport trunk native vlan 2"
        ))
    task.run(netmiko_send_config, config_commands=trunk_commands)


    # Place ports in default VLAN (1)
    interface_list = task.host['store']['facts']['interface_list']
    unused_port_config = []
    for interface in interface_list:
       if interface not in trunk_port_list:
           unused_port_config.extend((f'interface {interface}', 'no switchport access vlan'))
    task.run(netmiko_send_config, config_commands=unused_port_config)


    # Save configuration
    task.run(netmiko_send_command, command_string='write')



def main() -> None:
    nr = InitNornir('nornir_config/config.yaml')
    result = nr.run(task=deployment)
    print_result(result)

if __name__ == '__main__':
    main()
