local M = {
  "nvim-tree/nvim-tree.lua",
	dependencies = {
		"nvim-tree/nvim-web-devicons"
	}
}

M.config = function()
	require("nvim-tree").setup {}
end

return { M }