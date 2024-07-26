from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RbCls:
	"""Rb commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rb", core, parent)

	@property
	def auto(self):
		"""auto commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_auto'):
			from .Auto import AutoCls
			self._auto = AutoCls(self._core, self._cmd_group)
		return self._auto

	def set(self, no_rbs: int, start_rb: int, no_rb_cluster: int = None, start_rb_cluster: int = None, carrierComponent=repcap.CarrierComponent.Nr1, allocation=repcap.Allocation.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:ALLocation<Allocation>:PUSCh:RB \n
		Snippet: driver.configure.nrSubMeas.cc.allocation.pusch.rb.set(no_rbs = 1, start_rb = 1, no_rb_cluster = 1, start_rb_cluster = 1, carrierComponent = repcap.CarrierComponent.Nr1, allocation = repcap.Allocation.Default) \n
		No command help available \n
			:param no_rbs: No help available
			:param start_rb: No help available
			:param no_rb_cluster: No help available
			:param start_rb_cluster: No help available
			:param carrierComponent: optional repeated capability selector. Default value: Nr1
			:param allocation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Allocation')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('no_rbs', no_rbs, DataType.Integer), ArgSingle('start_rb', start_rb, DataType.Integer), ArgSingle('no_rb_cluster', no_rb_cluster, DataType.Integer, None, is_optional=True), ArgSingle('start_rb_cluster', start_rb_cluster, DataType.Integer, None, is_optional=True))
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		allocation_cmd_val = self._cmd_group.get_repcap_cmd_value(allocation, repcap.Allocation)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponent_cmd_val}:ALLocation{allocation_cmd_val}:PUSCh:RB {param}'.rstrip())

	# noinspection PyTypeChecker
	class RbStruct(StructBase):
		"""Response structure. Fields: \n
			- No_Rbs: int: No parameter help available
			- Start_Rb: int: No parameter help available
			- No_Rb_Cluster: int: No parameter help available
			- Start_Rb_Cluster: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('No_Rbs'),
			ArgStruct.scalar_int('Start_Rb'),
			ArgStruct.scalar_int('No_Rb_Cluster'),
			ArgStruct.scalar_int('Start_Rb_Cluster')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.No_Rbs: int = None
			self.Start_Rb: int = None
			self.No_Rb_Cluster: int = None
			self.Start_Rb_Cluster: int = None

	def get(self, carrierComponent=repcap.CarrierComponent.Nr1, allocation=repcap.Allocation.Default) -> RbStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:ALLocation<Allocation>:PUSCh:RB \n
		Snippet: value: RbStruct = driver.configure.nrSubMeas.cc.allocation.pusch.rb.get(carrierComponent = repcap.CarrierComponent.Nr1, allocation = repcap.Allocation.Default) \n
		No command help available \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1
			:param allocation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Allocation')
			:return: structure: for return value, see the help for RbStruct structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		allocation_cmd_val = self._cmd_group.get_repcap_cmd_value(allocation, repcap.Allocation)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponent_cmd_val}:ALLocation{allocation_cmd_val}:PUSCh:RB?', self.__class__.RbStruct())

	def clone(self) -> 'RbCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RbCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
