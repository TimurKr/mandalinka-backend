import Link from "next/link";

interface Props {
  href?: string;
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  type?: "submit" | "button" | "reset";
  style: "primary" | "secondary" | "black" | "danger" | "warning" | "success";
  dark?: boolean;
  disabled?: boolean;
  className?: string;
  children: React.ReactNode;
}

const Button = (props: Props) => {
  if (props.href && (props.onClick || props.type)) {
    throw new Error("Button cannot have href and onClick or type");
  } else if (!props.href && !props.onClick && !props.type) {
    throw new Error("Button must have href, onClick or type");
  }

  const className = `${props.className ? props.className : ""} btn ${
    props.style === "primary"
      ? props.dark
        ? "btn-primary-dark"
        : "btn-primary"
      : props.style === "secondary"
      ? props.dark
        ? "btn-secondary-dark"
        : "btn-secondary"
      : props.style === "black"
      ? props.dark
        ? "btn-black-dark"
        : "btn-black"
      : props.style === "danger"
      ? props.dark
        ? "btn-danger-dark"
        : "btn-danger"
      : props.style === "warning"
      ? props.dark
        ? "btn-warning-dark"
        : "btn-warning"
      : props.style === "success"
      ? props.dark
        ? "btn-success-dark"
        : "btn-success"
      : ""
  }`;

  if (props.href) {
    return (
      <Link href={props.href} className={className}>
        {props.children}
      </Link>
    );
  } else {
    return (
      <button
        type={props.type}
        className={className}
        onClick={props.onClick}
        disabled={props.disabled}
      >
        {props.children}
      </button>
    );
  }
};

export default Button;
