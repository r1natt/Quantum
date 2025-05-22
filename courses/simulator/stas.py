# from ipywidgets import interact
import matplotlib
matplotlib.use('Agg')  # Использовать неинтерактивный бэкенд
from matplotlib import pyplot as plt
import time
from sequence.kernel.timeline import Timeline
from sequence.topology.node import QuantumRouter, BSMNode
from sequence.components.optical_channel import QuantumChannel, ClassicalChannel
from sequence.constants import MILLISECOND

RAW_FIDELITY = 0.95
REQUEST_FIDELITY = 0.8

def test(sim_time, cc_delay, qc_atten, qc_dist):
    """
    sim_time: duration of simulation time (ms)
    cc_delay: delay on classical channels (ms)
    qc_atten: attenuation on quantum channels (dB/m)
    qc_dist: distance of quantum channels (km)
    """
    
    PS_PER_MS = 1e9
    M_PER_KM = 1e3
    
    # convert units for cc delay (to ps) and qc distance (to m)
    cc_delay *= PS_PER_MS
    qc_dist *= M_PER_KM
    
    # construct the simulation timeline; the constructor argument is the simulation time (in ps)
    tl = Timeline(sim_time * PS_PER_MS)
    
    ## create our quantum network and update parameters as needed
    
    # first, construct the quantum routers
    # (with arguments for the node name, timeline, and number of quantum memories)
    r1 = QuantumRouter("r1", tl, 50)
    r2 = QuantumRouter("r2", tl, 100)
    r3 = QuantumRouter("r3", tl, 50)
    # next, construct the BSM nodes
    # (with arguments for the node name, timeline, and the names of connected routers)
    m1 = BSMNode("m1", tl, ["r1", "r2"])
    m2 = BSMNode("m2", tl, ["r2", "r3"])
    
    r1.add_bsm_node(m1.name, r2.name)
    r2.add_bsm_node(m1.name, r1.name)
    r2.add_bsm_node(m2.name, r3.name)
    r3.add_bsm_node(m2.name, r2.name)
    
    # set seeds for random generators
    nodes = [r1, r2, r3, m1, m2]
    for i, node in enumerate(nodes):
        node.set_seed(i)
    
    for node in [r1, r2, r3]:
        memory_array = node.get_components_by_type("MemoryArray")[0]
        # we update the coherence time (measured in seconds) here
        memory_array.update_memory_params("coherence_time", 10)
        # and similarly update the fidelity of entanglement for the memories
        memory_array.update_memory_params("raw_fidelity", RAW_FIDELITY)
    
    # create all-to-all classical connections
    for node1 in nodes:
        for node2 in nodes:
            if node1 == node2:
                continue
            # construct a classical communication channel
            # (with arguments for the channel name, timeline, length (in m), and delay (in ps))
            cc = ClassicalChannel("cc_%s_%s"%(node1.name, node2.name), tl, 1e3, delay=cc_delay)
            cc.set_ends(node1, node2.name)
            
    # create quantum channels linking r1 and r2 to m1
    # (with arguments for the channel name, timeline, attenuation (in dB/m), and distance (in m))
    qc0 = QuantumChannel("qc_r1_m1", tl, qc_atten, qc_dist)
    qc1 = QuantumChannel("qc_r2_m1", tl, qc_atten, qc_dist)
    qc0.set_ends(r1, m1.name)
    qc1.set_ends(r2, m1.name)
    # create quantum channels linking r2 and r3 to m2
    qc2 = QuantumChannel("qc_r2_m2", tl, qc_atten, qc_dist)
    qc3 = QuantumChannel("qc_r3_m2", tl, qc_atten, qc_dist)
    qc2.set_ends(r2, m2.name)
    qc3.set_ends(r3, m2.name)

    # create routing table manually
    # note that the routing table is based on quantum links, not classical
    # the arguments are the names of the destination node and the next node in the best path towards the destination
    r1.network_manager.protocol_stack[0].add_forwarding_rule("r2", "r2")
    r1.network_manager.protocol_stack[0].add_forwarding_rule("r3", "r2")
    r2.network_manager.protocol_stack[0].add_forwarding_rule("r1", "r1")
    r2.network_manager.protocol_stack[0].add_forwarding_rule("r3", "r3")
    r3.network_manager.protocol_stack[0].add_forwarding_rule("r1", "r2")
    r3.network_manager.protocol_stack[0].add_forwarding_rule("r2", "r2")
    
    ## run our simulation
    
    tl.init()
    # we use the network manager of an end router to make our entanglement request
    # here, the arguments are:
    # (1) the destination node name,
    # (2) the start time (in ps) of entanglement,
    # (3) the end time (in ps) of entanglement,
    # (4) the number of memories to entangle, and
    # (5) the desired fidelity of entanglement.
    r1.network_manager.request("r3", 0.1e12, 10e12, 50, REQUEST_FIDELITY)

    tick = time.time()
    tl.run()
    print("execution time %.2f sec" % (time.time() - tick))
    
    ## display metrics for entangled memories and fidelities
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.set_size_inches(12, 8)

    # entangled memories on r1
    data = []
    for info in r1.resource_manager.memory_manager:
        if info.entangle_time > 0:
            data.append(info.entangle_time / MILLISECOND)
    data.sort()
    ax1.plot(data, range(1, len(data) + 1), marker="o")
    ax1.set_title("r1 - Entangled Memories")
    ax1.set_ylabel("Number of Entangled Memories")
    ax1.set_xlabel("Simulation Time (ms)")
    
    # entangled memories on r3
    data = []
    for info in r3.resource_manager.memory_manager:
        if info.entangle_time > 0:
            data.append(info.entangle_time / MILLISECOND)
    data.sort()
    ax2.plot(data, range(1, len(data) + 1), marker="o")
    ax2.set_title("r3 - Entangled Memories")
    ax2.set_xlabel("Simulation Time (ms)")
    
    # memory fidelities on r1
    data = []
    for info in r1.resource_manager.memory_manager:
        data.append(info.fidelity)
    ax3.bar(range(len(data)), data)
    ax3.plot([0, len(data)], [RAW_FIDELITY, RAW_FIDELITY], "--")
    ax3.plot([0, len(data)], [REQUEST_FIDELITY, REQUEST_FIDELITY], "--", color='red')
    ax3.set_ylim(0.7,1)
    ax3.set_title("r1 - Memory Fidelities")
    ax3.set_ylabel("Fidelity")
    ax3.set_xlabel("Memory Number")

    # memory fidelities on r3
    data = []
    for info in r3.resource_manager.memory_manager:
        data.append(info.fidelity)
    ax4.bar(range(len(data)), data)
    ax4.plot([0, len(data)], [RAW_FIDELITY, RAW_FIDELITY], "--")
    ax4.plot([0, len(data)], [REQUEST_FIDELITY, REQUEST_FIDELITY], "--", color='red')
    ax4.set_ylim(0.7,1)
    ax4.set_title("r3 - Memory Fidelities")
    ax4.set_xlabel("Memory Number")

    fig.tight_layout()
    return fig

# print(test(150, 0.5, 3e-5, 5))