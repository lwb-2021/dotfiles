local M = {
	"navarasu/onedark.nvim"
}

M.config = function()
	require('onedark').setup {
		style = "darker"
		
	}
	require('onedark').load()
end

return { M }