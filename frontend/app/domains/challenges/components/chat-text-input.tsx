import { ChevronUpIcon } from "lucide-react"
import { ChangeEvent, useEffect, useId, useRef } from "react"
import { Button } from "~/components/ui/button"

export interface ChatTextInputProps {
	disabled?: boolean
	value: string
	onChange: (value: string) => void
	onSubmit: () => void
}

export default (props: ChatTextInputProps) => {
	const areaId = useId()
	const areaRef = useRef<HTMLTextAreaElement>(null)
	const defaultRows = 1
	const maxRows = 4

	function onChange(event: ChangeEvent<HTMLTextAreaElement>) {
		const area = event.target

		area.style.height = "auto"

		const style = window.getComputedStyle(area)
		const borderHeight =
			Number.parseInt(style.borderTopWidth) +
			Number.parseInt(style.borderBottomWidth)
		const paddingHeight =
			Number.parseInt(style.paddingTop) + Number.parseInt(style.paddingBottom)

		const lineHeight = Number.parseInt(style.lineHeight)
		const maxHeight = maxRows
			? lineHeight * maxRows + borderHeight + paddingHeight
			: Number.POSITIVE_INFINITY

		area.style.height = `${Math.min(area.scrollHeight, maxHeight)}px`

		props.onChange(event.target.value)
	}

	function onKeyDown(event: React.KeyboardEvent<HTMLTextAreaElement>) {
		if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
			event.preventDefault()
			handleSubmit()
		}
	}

	function handleSubmit() {
		if (props.value.trim().length === 0) return

		props.onSubmit()
	}

	return (
		<div className="flex items-center justify-between max-w-3xl w-full bg-white space-x-2 mb-6 p-2 rounded-lg shadow border border-gray-200">
			<textarea
				id={areaId}
				ref={areaRef}
				value={props.value}
				placeholder="Ask questions about the challenge or type the flag..."
				onChange={onChange}
				onKeyDown={onKeyDown}
				rows={defaultRows}
				className="w-full flex-1 outline-none resize-none p-2"
				disabled={props.disabled}
			/>
			<div className="flex items-center justify-end">
				<Button disabled={props.disabled} size="icon" onClick={handleSubmit}>
					<ChevronUpIcon />
				</Button>
			</div>
		</div>
	)
}
