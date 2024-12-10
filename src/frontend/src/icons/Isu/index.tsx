import React, { forwardRef } from "react";
import SvgIsu from "./Isu";

export const IsuIcon = forwardRef<
  SVGSVGElement,
  React.PropsWithChildren<{}>
>((props, ref) => {
  return <SvgIsu ref={ref} {...props} />;
});
