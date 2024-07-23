from wiliot_deployment_tools.common.debug import debug_print
from wiliot_deployment_tools.interface.pkt_generator import BrgPktGeneratorNetwork
from wiliot_deployment_tools.interface.if_defines import *
from wiliot_deployment_tools.interface.packet_error import PacketError
import pkg_resources
import pandas as pd

CSV_NAME = 'packet_table.csv'
PACKET_TABLE_CSV_PATH = pkg_resources.resource_filename(__name__, CSV_NAME)

TEST_STRESS = 'stress'
TEST_COUPLING = 'coupling'
TEST_DOWNLINK = 'downlink'
TEST_UPLINK = 'uplink'
TEST_UNIFIED = 'unified'
TEST_SENSOR = 'sensor'

TESTS = [TEST_COUPLING, TEST_UPLINK, TEST_UNIFIED]
class GeneratedPacketTable:
    
    def __init__(self) -> None:
        self.brg_network = BrgPktGeneratorNetwork()
        self.table = pd.read_csv(PACKET_TABLE_CSV_PATH)
    
    def get_data(self, test, duplication, time_delay, bridge_idx) -> list:    
        assert test in TESTS, 'Invalid Test'
        assert (duplication in UPLINK_DUPLICATIONS) or (duplication in UNIFIED_DUPLICATIONS), 'Invalid Duplication'
        assert (time_delay in UPLINK_TIME_DELAYS) or (time_delay in UNIFIED_TIME_DELAYS), 'Invalid Time Delay'
        assert bridge_idx in BRIDGES, 'Invalid Bridge'
        
        t = self.table
        return t.loc[((t['test'] == test) &
                      (t['duplication']==duplication) &
                      (t['time_delay'] == time_delay) &
                      (t['bridge_idx'] == bridge_idx))].to_dict('records')[0]
            
    def get_df(self, columns=None):
        if columns is not None:
            return self.table[columns]
        return self.table
    
    def get_stress_data(self) -> pd.DataFrame:
        t = self.table
        return t.loc[((t['test'] == 'stress'))] 
    
    def get_sensor_data(self) -> pd.DataFrame:
        t = self.table
        return t.loc[((t['test'] == 'sensor'))] 
    
    def _generate_packet_table(self):
        packet_list = []
        
        # UPLINK TEST
        for duplication in UPLINK_DUPLICATIONS:
            debug_print(f'Duplication {duplication}')
            for time_delay in UPLINK_TIME_DELAYS:
                debug_print(f'Time Delay {time_delay}')
                pkts = self.brg_network.get_new_pkt_pairs()
                for idx, brg in enumerate(self.brg_network.brg_list):
                    debug_print(f'Bridge {idx}')
                    data = pkts[idx]['data_packet']
                    si = pkts[idx]['si_packet']
                    brg_id = self.brg_network.brg_list[idx].bridge_id
                    # log the sent packet with relevant info from run
                    expected_pkt = brg.get_expected_uncoupled_mqtt()
                    for pkt in expected_pkt:
                        pkt.update({'duplication': duplication, 'time_delay': time_delay})
                    packet_list.append({'test': TEST_UPLINK,
                                        'duplication': duplication,
                                        'time_delay': time_delay,
                                        'bridge_idx': idx,
                                        'expected_mqtt': expected_pkt
                                        ,'data': data, 'si': si, 'bridge_id': brg_id,
                                        })
                    
        # UNIFIED TEST (BASED ON UPLINK TEST)
        for duplication in UNIFIED_DUPLICATIONS:
            debug_print(f'Duplication {duplication}')
            for time_delay in UNIFIED_TIME_DELAYS:
                debug_print(f'Time Delay {time_delay}')
                pkts = self.brg_network.get_new_pkt_unified()
                for idx, brg in enumerate(self.brg_network.brg_list):
                    debug_print(f'Bridge {idx}')
                    data = pkts[idx]['data_packet']
                    brg_id = self.brg_network.brg_list[idx].bridge_id
                    # log the sent packet with relevant info from run
                    expected_pkt = brg.get_expected_mqtt_unified(full_data_pkt=data)
                    for pkt in expected_pkt:
                        pkt.update({'duplication': duplication, 'time_delay': time_delay})
                    packet_list.append({'test': TEST_UNIFIED,
                                        'duplication': duplication,
                                        'time_delay': time_delay,
                                        'bridge_idx': idx,
                                        'expected_mqtt': expected_pkt
                                        ,'data': data, 'bridge_id': brg_id,
                                        })        

        #STRESS TEST
        i = 0
        while i < 5000:
            i += 1
            pkts = self.brg_network.get_new_pkt_unified()
            target_idx = 0  
            brg = self.brg_network.brg_list[target_idx]
            debug_print(f'Bridge {target_idx}')
            data = pkts[target_idx]['data_packet']
            brg_id = brg.bridge_id
            expected_pkt = brg.get_expected_mqtt_unified(full_data_pkt=data)
            packet_list.append({
                'test': TEST_STRESS,
                'bridge_idx': target_idx,
                'expected_mqtt': expected_pkt,
                'data': data,
                'bridge_id': brg_id,
            })          

        def _sensor_data(df):
            hardcoded_data = [
                {"test": "sensor", "duplication": "", "time_delay": "", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC020000B54D387A227038613C0D8E0FF376D199289FE6679AA0D902", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B87B44500000000000000000000009AA0D902", "duplication": 3, "time_delay": 20}], "data": "F0287B2557141E1690FC020000B54D387A227038613C0D8E0FF376D199289FE6679AA0D902", "si": "3B613D0817FB1E16C6FC0000EB3B613D08177B87B44500000000000000000000009AA0D902", "bridge_id": "3B613D08177B"},
                {"test": "sensor", "duplication": "", "time_delay": "", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC0200003A79C9BEF41223AC3F4A962D97F519C9DA06CA5F4F643826", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B7D396B00000000000000000000004F643826", "duplication": 3, "time_delay": 20}], "data": "F0287B2557141E1690FC0200003A79C9BEF41223AC3F4A962D97F519C9DA06CA5F4F643826", "si": "3B613D0817FB1E16C6FC0000EB3B613D08177B7D396B00000000000000000000004F643826", "bridge_id": "3B613D08177B"},
                {"test": "sensor", "duplication": "", "time_delay": "", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC0200001B65E90DDC0090175F67F3F8E7E3DA2FFA6A945076D1D979", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B39B69D000000000000000000000076D1D979", "duplication": 3, "time_delay": 20}], "data": "F0287B2557141E1690FC0200001B65E90DDC0090175F67F3F8E7E3DA2FFA6A945076D1D979", "si": "3B613D0817FB1E16C6FC0000EB3B613D08177B39B69D000000000000000000000076D1D979", "bridge_id": "3B613D08177B"},
                {"test": "sensor", "duplication": "", "time_delay": "", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC020000D337363E43CDDDFC897492917BCC2DA2977E2751E31CAAA6", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B3E21640000000000000000000000E31CAAA6", "duplication": 3, "time_delay": 20}], "data": "F0287B2557141E1690FC020000D337363E43CDDDFC897492917BCC2DA2977E2751E31CAAA6", "si": "3B613D0817FB1E16C6FC0000EB3B613D08177B3E21640000000000000000000000E31CAAA6", "bridge_id": "3B613D08177B"},
                {"test": "sensor", "duplication": "", "time_delay": "", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC0200001D646652892618D2CE80CA4A880A8CF46346C7743C509B54", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B5BCD2900000000000000000000003C509B54", "duplication": 3, "time_delay": 20}], "data": "F0287B2557141E1690FC0200001D646652892618D2CE80CA4A880A8CF46346C7743C509B54", "si": "3B613D0817FB1E16C6FC0000EB3B613D08177B5BCD2900000000000000000000003C509B54", "bridge_id": "3B613D08177B"},
                {"test": "sensor", "duplication": "", "time_delay": "", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC020000CEE15F2E2EE026B22C739867453C6E2E108E9E8610FE7F07", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B9647FC000000000000000000000010FE7F07", "duplication": 3, "time_delay": 20}], "data": "F0287B2557141E1690FC020000CEE15F2E2EE026B22C739867453C6E2E108E9E8610FE7F07", "si": "3B613D0817FB1E16C6FC0000EB3B613D08177B9647FC000000000000000000000010FE7F07", "bridge_id": "3B613D08177B"},
                {"test": "sensor", "duplication": "", "time_delay": "", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC0200002CC60917A02CB02367771BE9EA20F9666ED8A06F6612745B", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177BF1EBC500000000000000000000006612745B", "duplication": 3, "time_delay": 20}], "data": "F0287B2557141E1690FC0200002CC60917A02CB02367771BE9EA20F9666ED8A06F6612745B", "si": "3B613D0817FB1E16C6FC0000EB3B613D08177BF1EBC500000000000000000000006612745B", "bridge_id": "3B613D08177B"},
                {"test": "sensor", "duplication": "", "time_delay": "", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC02000007EFE229109B044DB995A506179C99094720AE8BF9F78C1A", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B6CEC9A0000000000000000000000F9F78C1A", "duplication": 3, "time_delay": 20}], "data": "F0287B2557141E1690FC02000007EFE229109B044DB995A506179C99094720AE8BF9F78C1A", "si": "3B613D0817FB1E16C6FC0000EB3B613D08177B6CEC9A0000000000000000000000F9F78C1A", "bridge_id": "3B613D08177B"},
                {"test": "sensor", "duplication": "", "time_delay": "", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC0200002CA1E008E364D0DCF65631718BCD659DE3323A69A674F7B9", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B1051900000000000000000000000A674F7B9", "duplication": 3, "time_delay": 20}], "data": "F0287B2557141E1690FC0200002CA1E008E364D0DCF65631718BCD659DE3323A69A674F7B9", "si": "3B613D0817FB1E16C6FC0000EB3B613D08177B1051900000000000000000000000A674F7B9", "bridge_id": "3B613D08177B"},
                {"test": "sensor", "duplication": "", "time_delay": "", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC02000049ADD722F535679C37983927655C974A4980B080045DA6C2", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B5280B20000000000000000000000045DA6C2", "duplication": 3, "time_delay": 20}], "data": "F0287B2557141E1690FC02000049ADD722F535679C37983927655C974A4980B080045DA6C2", "si": "3B613D0817FB1E16C6FC0000EB3B613D08177B5280B20000000000000000000000045DA6C2", "bridge_id": "3B613D08177B"},
                {"test": "sensor", "duplication": "", "time_delay": "", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC0200004C8AD49C6D96923BFB70DF06554F5E8F438F1DF57E063773", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177BB4085900000000000000000000007E063773", "duplication": 3, "time_delay": 20}], "data": "F0287B2557141E1690FC0200004C8AD49C6D96923BFB70DF06554F5E8F438F1DF57E063773", "si": "3B613D0817FB1E16C6FC0000EB3B613D08177BB4085900000000000000000000007E063773", "bridge_id": "3B613D08177B"},
                {"test": "sensor", "duplication": "", "time_delay": "", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC02000064A5B54285BB6BCDB457ABBED8EE26B4EB43B27A8C26781C", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B27363800000000000000000000008C26781C", "duplication": 3, "time_delay": 20}], "data": "F0287B2557141E1690FC02000064A5B54285BB6BCDB457ABBED8EE26B4EB43B27A8C26781C", "si": "3B613D0817FB1E16C6FC0000EB3B613D08177B27363800000000000000000000008C26781C", "bridge_id": "3B613D08177B"}
            ]
        
            hardcoded_df = pd.DataFrame(hardcoded_data)
            return pd.concat([df, hardcoded_df], ignore_index=True)
        
        df = pd.DataFrame(packet_list)
        df = _sensor_data(df)
        df.to_csv(PACKET_TABLE_CSV_PATH)

class CouplingRunData:
    def __init__(self, data) -> None:
        self.test = data['test']
        self.duplication = data['duplication']
        self.time_delay = data['time_delay']
        self.bridge_idx = data['bridge_idx']
        self.packet_error = eval(data['packet_error'])
        self.expected_mqtt = eval(data['expected_mqtt'])
        self.data = data['data']
        self.si = data['si']
        self.bridge_id = data['bridge_id']
        self.scattered_time_delay = data['scattered_time_delay']


    @classmethod
    def get_data(cls, test, duplication, time_delay, bridge_idx):
        packet_data = GeneratedPacketTable().get_data(test, duplication, time_delay, bridge_idx)
        return cls(packet_data)

class UplinkRunData:
    def __init__(self, data) -> None:
        self.test = data['test']
        self.duplication = data['duplication']
        self.time_delay = data['time_delay']
        self.bridge_idx = data['bridge_idx']
        self.expected_mqtt = eval(data['expected_mqtt'])
        self.data = data['data']
        self.si = data['si']
        self.bridge_id = data['bridge_id']   

    @classmethod
    def get_data(cls, test, duplication, time_delay, bridge_idx):
        packet_data = GeneratedPacketTable().get_data(test, duplication, time_delay, bridge_idx)
        return cls(packet_data)
    
class UnifiedRunData:
    def __init__(self, data) -> None:
        self.test = data['test']
        self.duplication = data['duplication']
        self.time_delay = data['time_delay']
        self.bridge_idx = data['bridge_idx']
        self.expected_mqtt = eval(data['expected_mqtt'])
        self.data = data['data']
        self.bridge_id = data['bridge_id']   

    @classmethod
    def get_data(cls, test, duplication, time_delay, bridge_idx):
        packet_data = GeneratedPacketTable().get_data(test, duplication, time_delay, bridge_idx)
        return cls(packet_data)
    
    @classmethod
    def get_df(cls, columns=None):
       df = GeneratedPacketTable().get_df(columns)
       return df[df['test'] == TEST_UNIFIED]


class StressRunData:
    def __init__(self) -> None:
        self.data = GeneratedPacketTable().get_stress_data()

class SensorRunData:
    def __init__(self) -> None:
        self.data = GeneratedPacketTable().get_sensor_data()
        
if __name__ == "__main__":
    GeneratedPacketTable()._generate_packet_table()
