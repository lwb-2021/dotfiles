local M = {
  'akinsho/bufferline.nvim', 
  dependencies = {'kyazdani42/nvim-web-devicons'}
}
M.config = function ()
  vim.opt.termguicolors = true
  require("bufferline").setup {
    options = {
        -- 使用 nvim 内置lsp
      diagnostics = "nvim_lsp",
        -- 左侧让出 nvim-tree 的位置
      offsets = {{
        filetype = "NvimTree",
        text = "File Explorer",
        highlight = "Directory",
        text_align = "left"
      }}
    }
  }
end
return {M}
