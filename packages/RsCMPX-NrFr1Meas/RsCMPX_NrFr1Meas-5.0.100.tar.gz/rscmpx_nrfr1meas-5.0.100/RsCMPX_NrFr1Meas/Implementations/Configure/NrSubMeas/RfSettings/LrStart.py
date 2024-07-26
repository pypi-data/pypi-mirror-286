from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LrStartCls:
	"""LrStart commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lrStart", core, parent)

	def set(self) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:RFSettings:LRSTart \n
		Snippet: driver.configure.nrSubMeas.rfSettings.lrStart.set() \n
		No command help available \n
		"""
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:RFSettings:LRSTart')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:RFSettings:LRSTart \n
		Snippet: driver.configure.nrSubMeas.rfSettings.lrStart.set_with_opc() \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCMPX_NrFr1Meas.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'CONFigure:NRSub:MEASurement<Instance>:RFSettings:LRSTart', opc_timeout_ms)
