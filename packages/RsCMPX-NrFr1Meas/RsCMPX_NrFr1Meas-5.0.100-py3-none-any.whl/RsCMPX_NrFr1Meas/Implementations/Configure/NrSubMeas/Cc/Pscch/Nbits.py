from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NbitsCls:
	"""Nbits commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nbits", core, parent)

	def set(self, user_defined: bool, no_symbols: int = None, carrierComponentOne=repcap.CarrierComponentOne.Nr1) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:PSCCh:NBITs \n
		Snippet: driver.configure.nrSubMeas.cc.pscch.nbits.set(user_defined = False, no_symbols = 1, carrierComponentOne = repcap.CarrierComponentOne.Nr1) \n
		No command help available \n
			:param user_defined: No help available
			:param no_symbols: No help available
			:param carrierComponentOne: optional repeated capability selector. Default value: Nr1
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('user_defined', user_defined, DataType.Boolean), ArgSingle('no_symbols', no_symbols, DataType.Integer, None, is_optional=True))
		carrierComponentOne_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponentOne, repcap.CarrierComponentOne)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponentOne_cmd_val}:PSCCh:NBITs {param}'.rstrip())

	# noinspection PyTypeChecker
	class NbitsStruct(StructBase):
		"""Response structure. Fields: \n
			- User_Defined: bool: No parameter help available
			- No_Symbols: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('User_Defined'),
			ArgStruct.scalar_int('No_Symbols')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.User_Defined: bool = None
			self.No_Symbols: int = None

	def get(self, carrierComponentOne=repcap.CarrierComponentOne.Nr1) -> NbitsStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:PSCCh:NBITs \n
		Snippet: value: NbitsStruct = driver.configure.nrSubMeas.cc.pscch.nbits.get(carrierComponentOne = repcap.CarrierComponentOne.Nr1) \n
		No command help available \n
			:param carrierComponentOne: optional repeated capability selector. Default value: Nr1
			:return: structure: for return value, see the help for NbitsStruct structure arguments."""
		carrierComponentOne_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponentOne, repcap.CarrierComponentOne)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponentOne_cmd_val}:PSCCh:NBITs?', self.__class__.NbitsStruct())
