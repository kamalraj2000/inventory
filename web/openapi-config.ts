import type { ConfigFile } from '@rtk-query/codegen-openapi'

const config: ConfigFile = {
  schemaFile: '../PythonApi/openapi.json',
  apiFile: './src/store/api/empty-api.ts',
  apiImport: 'emptySplitApi',
  outputFile: './src/store/api/generated/products.ts',
  exportName: 'productsApi',
  hooks: true,
}

export default config