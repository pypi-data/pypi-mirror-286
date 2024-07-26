from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DallocationCls:
	"""Dallocation commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dallocation", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability indicator'
			- Seg_Reliability: int: Reliability indicator for the segment
			- Nr_Res_Blocks: int: Number of allocated resource blocks
			- Offset_Res_Blocks: int: Offset of the first allocated resource block from the edge of the allocated transmission bandwidth"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_int('Nr_Res_Blocks'),
			ArgStruct.scalar_int('Offset_Res_Blocks')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Nr_Res_Blocks: int = None
			self.Offset_Res_Blocks: int = None

	def fetch(self, sEGMent=repcap.SEGMent.Default, carrierComponent=repcap.CarrierComponent.Default) -> FetchStruct:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>[:CC<Carrier>]:MODulation:DALLocation \n
		Snippet: value: FetchStruct = driver.nrSubMeas.multiEval.listPy.segment.cc.modulation.dallocation.fetch(sEGMent = repcap.SEGMent.Default, carrierComponent = repcap.CarrierComponent.Default) \n
		Return the detected allocation for segment <no> in list mode. The result is determined from the last measured slot of the
		statistical length. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:CC{carrierComponent_cmd_val}:MODulation:DALLocation?', self.__class__.FetchStruct())
