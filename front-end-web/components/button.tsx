import Link from "next/link";

interface Props extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  href?: string;
  color: "primary" | "secondary" | "black" | "danger" | "warning" | "success";
  dark?: boolean;
  className?: string;
}

const Button = (props: Props) => {
  const { style, dark, className = "", href, children, ...buttonProps } = props;

  if (href && (buttonProps.onClick || buttonProps.type)) {
    throw new Error("Button cannot have href and onClick or type");
  } else if (!href && !buttonProps.onClick && !buttonProps.type) {
    throw new Error("Button must have href, onClick or type");
  }

  const buttonClassName = `${className} btn ${
    props.color === "primary"
      ? props.dark
        ? "btn-primary-dark"
        : "btn-primary"
      : props.color === "secondary"
      ? props.dark
        ? "btn-secondary-dark"
        : "btn-secondary"
      : props.color === "black"
      ? props.dark
        ? "btn-black-dark"
        : "btn-black"
      : props.color === "danger"
      ? props.dark
        ? "btn-danger-dark"
        : "btn-danger"
      : props.color === "warning"
      ? props.dark
        ? "btn-warning-dark"
        : "btn-warning"
      : props.color === "success"
      ? props.dark
        ? "btn-success-dark"
        : "btn-success"
      : ""
  }`;

  if (href && !buttonProps.disabled) {
    return (
      <Link href={href} className={buttonClassName}>
        {children}
      </Link>
    );
  } else {
    return (
      <button className={buttonClassName} {...buttonProps}>
        {children}
      </button>
    );
  }
};

export default Button;
