# Application reproduction

This application uses the published mitt 3.0.1 package. Its desired operation is to stop wildcard subscriptions while keeping named subscriptions active.

The TypeScript input is `task.ts`. Run the existing local compiler:

```sh
node node_modules/typescript/bin/tsc task.ts --noEmit --strict --lib es2015 --moduleResolution node
```

The sibling library source and its original README are supplied in the parent directory. The consumer has its own installed package; a direct source import is not this application's normal entry point.
